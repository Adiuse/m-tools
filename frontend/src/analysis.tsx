import { useEffect, useState } from 'react';
import { api, errorText } from './api';
import type { Draft, Method, Ref, RunRequest, Translate, Workspace } from './api';
import { Field, formValues, Message, useTask } from './shared';

const names: Record<string, [string, string]> = {
  S01:['تشخیص مسئله','Problem diagnosis'], S02:['مدل کسب‌وکار','Business model'], S03:['انتخاب استراتژیک','Strategic choice'],
  S04:['اولویت‌بندی','Prioritization'], S05:['تحلیل سناریو','Scenarios'], S06:['ورود به بازار','Go-to-market'],
  M01:['تحقیق بازار','Market research'], M02:['اندازه بازار','Market sizing'], M03:['تحلیل رقبا','Competitor analysis'],
  M04:['تحلیل کیفی','Qualitative analysis'], M05:['بخش‌بندی','Segmentation'], M06:['جایگاه‌سازی','Positioning'],
  M07:['تناسب محصول و بازار','Product–market fit'], M08:['ارزیابی برند','Brand audit'], M09:['سفر مشتری','Customer journey'],
  B01:['اقتصاد مشتری','Unit economics'], B02:['قیمت و تقاضا','Pricing and demand'], B03:['قیف و ریزش','Funnel and churn'],
  B04:['آزمون و تحلیل علّی','Experiment and causality'], B05:['شاخص‌های عملکرد','Performance metrics'], B06:['تخصیص منابع','Resource allocation'],
  E01:['برنامهٔ یکپارچه','Integrated plan'], E02:['کمپین','Campaign'], E03:['کانال و رسانه','Channel and media'],
  E04:['چرخهٔ مشتری','Customer lifecycle'], E05:['عملیات','Operations'], E06:['مسئولیت‌ها','Responsibilities'],
  E07:['ذی‌نفعان','Stakeholders'], E08:['بازبینی و یادگیری','Review and learning'],
  QT01:['هزینهٔ جذب مشتری','Customer acquisition cost'], QT02:['بازده هزینهٔ تبلیغات','Return on ad spend'],
  QT03:['حاشیهٔ سود','Margin'], QT04:['نقطهٔ سربه‌سر','Break-even'], QT05:['سناریوی قیمت','Price scenarios'],
  QT06:['نرخ تبدیل قیف','Funnel conversion'], QT07:['نرخ ریزش','Churn'], QT08:['حجم نمونهٔ پیمایش','Survey sample size'],
  QT09:['شکاف عملکرد','Performance gap'], QT10:['بازده سرمایه‌گذاری بازاریابی','Return on marketing investment'],
  QT11:['شاخص‌های رسانه','Media metrics'], QT12:['اندازهٔ بازار','Addressable market'], QT13:['توان آزمون','Test power'],
  QT14:['ارزش طول عمر مشتری','Customer lifetime value'], QT15:['دورهٔ بازگشت هزینهٔ جذب','Acquisition payback'],
};
const catalogId = (method: Method) => method.quick ? method.method_id : method.tool_id;
const title = (tool: string, t: Translate) => names[tool] ? t(...names[tool]) : tool;
const availabilityLabel = (availability: string, t: Translate) =>
  availability === 'planned' ? t('برنامه‌ریزی‌شده', 'Planned') : availability;

type JSONProperty = {
  type?: string; format?: string; enum?: (string | number)[]; anyOf?: JSONProperty[];
  properties?: Record<string, JSONProperty>; required?: string[]; $ref?: string;
  minimum?: number; maximum?: number;
};
type InputSchema = { $ref: string; $defs: Record<string, JSONProperty> };
type ToolDetail = { methods: Method[]; schemas: Record<string, InputSchema> };
type Preflight = { availability: string; required_for_primary: string[]; missing_fields: string[]; limitations: string[] };
type SourceVersions = { stale: boolean; refs: (Ref & { latest_version: number | null })[] };
type Result = { run_id: string; tool_id: string; method_id: string; method_version: number;
  status: string; analysis_status: string | null;
  limitations: string[]; findings: { statement: string; kind: string }[]; next_action: string | null;
  options: { id: string; title: string }[] };
type Decision = { id: string; run_id: string; selected_option: string; reason: string; state: string };
type EvidenceChoice = { id: string; version: number; title: string };

export function Catalog({ methods, current, select, t }: {
  methods: Method[]; current: string; select: (tool: string) => void; t: Translate;
}) {
  const [query, setQuery] = useState('');
  const [scope, setScope] = useState('all');
  const tools = [...new Map(methods.map((method) => [catalogId(method), method])).values()]
    .filter((method) => scope === 'all' || method.quick === (scope === 'quick'))
    .filter((method) => ([catalogId(method), ...(names[catalogId(method)] ?? [])].join(' ')).toLowerCase().includes(query.toLowerCase()));
  return <section className="panel catalog">
    <h2>{t('کاتالوگ ابزارها', 'Tool catalog')}</h2>
    <Field label={t('جست‌وجو', 'Search')}><input type="search" value={query} onChange={(event) => setQuery(event.target.value)} /></Field>
    <Field label={t('نوع ابزار', 'Tool type')}><select value={scope} onChange={(event) => setScope(event.target.value)}>
      <option value="all">{t('همه', 'All')}</option><option value="full">{t('ابزارهای اصلی', 'Professional tools')}</option>
      <option value="quick">{t('ابزارهای سریع', 'Quick tools')}</option>
    </select></Field>
    <ul className="record-list">{tools.map((method) => <li key={catalogId(method)}>
      <button className="record" aria-current={current === catalogId(method) ? 'true' : undefined} onClick={() => select(catalogId(method))}>
        <span><bdi className="tool-code">{catalogId(method)}</bdi> {title(catalogId(method), t)}</span>
        <small>{availabilityLabel(method.availability, t)}</small>
      </button></li>)}</ul>
  </section>;
}

function SchemaFields({ schema, input, setInput, t, required = [] }: {
  schema: InputSchema; input: Record<string, unknown>; setInput: (data: Record<string, unknown>) => void;
  t: Translate; required?: string[];
}) {
  const definition = schema.$defs[schema.$ref.split('/').at(-1) ?? ''];
  const properties = definition?.properties ?? {};
  const priority = new Set([...(definition?.required ?? []), ...required]);
  const entries = Object.entries(properties).sort(([left], [right]) =>
    Number(priority.has(right)) - Number(priority.has(left)));
  function update(key: string, value: unknown) {
    const next = { ...input };
    if (value === undefined) delete next[key];
    else next[key] = value;
    setInput(next);
  }
  return <>{entries.map(([key, spec]) => <SchemaField key={key} label={key.replaceAll('_', ' ')}
    spec={spec} definitions={schema.$defs} value={input[key]} onChange={(value) => update(key, value)} t={t} />)}</>;
}

function SchemaField({ label, spec, definitions, value, onChange, t }: {
  label: string; spec: JSONProperty; definitions: InputSchema['$defs']; value: unknown;
  onChange: (value: unknown) => void; t: Translate;
}) {
  if (spec.$ref) spec = definitions[spec.$ref.split('/').at(-1) ?? ''] ?? spec;
  if (spec.anyOf) {
    const nonNull = spec.anyOf.filter((option) => option.type !== 'null');
    if (nonNull.length === 1) return <SchemaField label={label} spec={nonNull[0]} definitions={definitions}
      value={value} onChange={onChange} t={t} />;
  }
  if (spec.type === 'object' && spec.properties) {
    const record = value && typeof value === 'object' && !Array.isArray(value) ? value as Record<string, unknown> : {};
    return <details className="inset"><summary>{label}</summary>
      {Object.entries(spec.properties).map(([key, child]) => <SchemaField key={key} label={key.replaceAll('_', ' ')}
        spec={child} definitions={definitions} value={record[key]} onChange={(next) => {
          const updated = { ...record };
          if (next === undefined) delete updated[key];
          else updated[key] = next;
          onChange(Object.keys(updated).length ? updated : undefined);
        }} t={t} />)}
    </details>;
  }
  const choices = spec.enum ?? (spec.type === 'boolean' ? ['true', 'false'] : undefined);
  if (choices) return <Field label={label}><select value={String(value ?? '')} onChange={(event) => {
    const selected = event.target.value;
    onChange(selected === '' ? undefined : spec.type === 'boolean' ? selected === 'true'
      : choices.find((option) => String(option) === selected));
  }}>
    <option value="">{t('انتخاب کنید', 'Select')}</option>
    {choices.map((option) => <option key={option}>{option}</option>)}
  </select></Field>;
  const number = spec.type === 'integer' || spec.type === 'number';
  if (!number && spec.type !== 'string') return null;
  return <Field label={label}><input type={number ? 'number' : spec.format === 'date' ? 'date' : 'text'}
    step={spec.type === 'number' ? 'any' : undefined} min={spec.minimum} max={spec.maximum}
    value={String(value ?? '')} onChange={(event) => {
      const next = event.target.value;
      onChange(next === '' ? undefined : number ? Number(next) : next);
    }} /></Field>;
}

function Decisions({ result, workspace, t }: { result: Result; workspace: Workspace; t: Translate }) {
  const path = '/workspaces/' + workspace.id + '/decisions';
  const [items, setItems] = useState<Decision[]>([]);
  const task = useTask(t);
  const [loadError, setLoadError] = useState('');
  useEffect(() => {
    let current = true;
    api<Decision[]>(path)
      .then((data) => { if (current) setItems(data); })
       .catch((cause) => { if (current) setLoadError(errorText(cause, t)); });
    return () => { current = false; };
  }, [path, t]);
  if (result.status !== 'succeeded' || !result.options.length) return null;
  const replace = (next: Decision) => setItems((previous) => [next, ...previous.filter((item) => item.id !== next.id)]);
  return <section>
    <h3>{t('تصمیم‌ها', 'Decisions')}</h3>
    {workspace.role !== 'viewer' && <form onSubmit={(event) => {
      const values = formValues(event);
      task.run(async () => replace(await api<Decision>(path, 'POST', { ...values, run_id: result.run_id })));
    }}>
      <Field label={t('گزینهٔ پیشنهادی', 'Proposed option')}><select name="selected_option" required>
        {result.options.map((option) => <option key={option.id} value={option.id}>{option.title}</option>)}
      </select></Field>
      <Field label={t('دلیل انتخاب', 'Decision rationale')}><textarea name="reason" maxLength={500} required /></Field>
      <button className="secondary" disabled={task.busy}>{t('ثبت تصمیم پیشنهادی', 'Save proposed decision')}</button>
    </form>}
    <Message text={task.error || loadError} error />
    <ul className="record-list">{items.filter((item) => item.run_id === result.run_id).map((item) =>
      <li className="history-row" key={item.id}>
        <span>{item.reason}</span><small>{item.state === 'approved' ? t('تأییدشده', 'Approved') : t('پیش‌نویس', 'Draft')}</small>
        {workspace.role === 'owner' && item.state === 'draft' && <button className="secondary" disabled={task.busy}
          onClick={() => task.run(async () => replace(await api<Decision>(path + '/' + item.id + '/approve', 'POST', {})))}>
          {t('تأیید تصمیم', 'Approve decision')}
        </button>}
      </li>)}</ul>
  </section>;
}

export function AnalysisPage({ workspace, methods, t, onDirty, visible = true }: {
  workspace?: Workspace; methods: Method[]; t: Translate; onDirty: (dirty: boolean) => void; visible?: boolean;
}) {
  const base = workspace ? '/workspaces/' + workspace.id : '';
  const [tool, setTool] = useState('');
  const [methodId, setMethod] = useState('');
  const [detail, setDetail] = useState<ToolDetail>();
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [selected, setSelected] = useState<Draft>();
  const [evidence, setEvidence] = useState<EvidenceChoice[]>([]);
  const [sources, setSources] = useState<Ref[]>([]);
  const [runs, setRuns] = useState<Result[]>([]);
  const [result, setResult] = useState<Result>();
  const [versions, setVersions] = useState<SourceVersions>();
  const [question, setQuestion] = useState('');
  const [raw, setRaw] = useState('{}');
  const [check, setCheck] = useState<Preflight>();
  const [notice, setNotice] = useState('');
  const [loadError, setLoadError] = useState('');
  const [requestKey, setRequestKey] = useState(() => crypto.randomUUID());
  const [dirty, setDirty] = useState(false);
  const task = useTask(t);
  const method = detail?.methods.find((item) => item.method_id === methodId) ?? detail?.methods[0];
  const schema = method ? detail?.schemas[method.method_id] : undefined;
  const evidenceChoices = [...evidence, ...sources.filter((ref) => !evidence.some((item) => item.id === ref.id))
    .map((ref) => ({ id: ref.id, version: ref.version, title: ref.id }))];
  const canSave = workspace && workspace.role !== 'viewer' && !method?.quick;
  const newerDraft = selected && drafts.some((item) => item.series === selected.series && item.version > selected.version);
  let parsed: Record<string, unknown> = {};
  try { parsed = JSON.parse(raw); } catch { /* Validate when submitted. */ }

  useEffect(() => {
    if (!tool) return;
    let current = true;
    api<ToolDetail>('/tools/' + tool).then((data) => { if (current) setDetail(data); })
      .catch((error) => { if (current) setLoadError(errorText(error, t)); });
    return () => { current = false; };
  }, [tool, t]);

  useEffect(() => {
    if (!base || !visible) return;
    let current = true;
    Promise.all([api<Draft[]>(base + '/drafts'), api<EvidenceChoice[]>(base + '/entities/evidence'), api<Result[]>(base + '/runs')])
      .then(([draftRows, evidenceRows, runRows]) => {
        if (current) { setDrafts(draftRows); setEvidence(evidenceRows); setRuns(runRows); }
      }).catch((error) => { if (current) setLoadError(errorText(error, t)); });
    return () => { current = false; };
  }, [base, t, visible]);

  function mark(changed: boolean) {
    setDirty(changed);
    if (canSave) onDirty(changed);
    if (changed) { setCheck(undefined); setNotice(''); setRequestKey(crypto.randomUUID()); }
  }

  function canDiscard() {
    return !dirty || window.confirm(t('تغییرات ذخیره نشده‌اند. ادامه می‌دهید؟', 'Discard unsaved changes?'));
  }

  function choose(id: string, draft?: Draft) {
    if (task.busy || !canDiscard()) return;
    setDetail(undefined); setTool(id); setMethod(draft?.request.method_id ?? '');
    setSelected(draft); setQuestion(draft?.request.question ?? '');
    setSources(draft?.request.evidence_refs ?? []);
    setRaw(JSON.stringify(draft?.request.input ?? {}, null, 2)); setResult(undefined); setVersions(undefined);
    setCheck(undefined); setNotice(''); setLoadError(''); mark(false); setRequestKey(crypto.randomUUID());
  }

  function submit(mode: 'check' | 'save') {
    task.run(async () => {
      let input: Record<string, unknown>;
      try {
        input = JSON.parse(raw);
        if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error();
      } catch {
        setNotice(t('ورودی باید یک شیء JSON معتبر باشد.', 'Enter a valid JSON object.'));
        return;
      }
      if (!method) return;
      if (method.quick) {
        await api('/scratch', 'POST', { quick_id: method.method_id, method_version: method.method_version, input });
        return;
      }
      if (!workspace) return;
      const body: RunRequest = {
        workspace_id: workspace.id, tool_id: method.tool_id, method_id: method.method_id,
        method_version: method.method_version, question, input, evidence_refs: sources,
        dependency_run_ids: selected?.request.dependency_run_ids ?? [], idempotency_key: requestKey,
      };
      if (mode === 'check') {
        setCheck(await api<Preflight>(base + '/preflight', 'POST', body));
      } else {
        const changed = await api<Draft>(base + '/drafts' + (selected ? '/' + selected.id : ''), selected ? 'PATCH' : 'POST', body);
        setDrafts((previous) => [changed, ...previous.filter((draft) => draft.id !== changed.id)]);
        setSelected(changed); mark(false); setRequestKey(crypto.randomUUID());
        setNotice(t('پیش‌نویس ذخیره شد.', 'Draft saved.'));
      }
    });
  }

  return <div className="split analysis-layout">
    <section className="panel">
      <h2>{tool ? title(tool, t) : t('تحلیل و پیش‌نویس‌ها', 'Analysis and drafts')}</h2>
      <Message text={task.error || loadError} error /><Message text={notice} />
      {method && <fieldset className="analysis-fields" disabled={task.busy}>
        {detail && detail.methods.length > 1 && <Field label={t('روش', 'Method')}><select value={method.method_id}
          onChange={(event) => {
            if (canDiscard()) { setMethod(event.target.value); setRaw('{}'); mark(true); }
          }}>
          {detail.methods.map((item) => <option key={item.method_id} value={item.method_id}>{item.method_id} · v{item.method_version}</option>)}
        </select></Field>}
        <p className="status-tag">{availabilityLabel(method.availability, t)}</p>
        {!method.quick && workspace && <>
          <Field label={t('سؤال تحلیل', 'Analysis question')}><textarea value={question} maxLength={1200}
            onChange={(event) => { setQuestion(event.target.value); mark(true); }} /></Field>
          <Field label={t('شواهد و نسخه‌ها', 'Evidence and versions')}><select multiple value={sources.map((ref) => ref.id)}
            onChange={(event) => {
              const picked = Array.from(event.target.selectedOptions, (option) => option.value);
              setSources(evidenceChoices.filter((row) => picked.includes(row.id))
                .map((row) => ({ kind: 'evidence', id: row.id, version: row.version })));
              mark(true);
            }}>
            {evidenceChoices.map((row) => <option key={row.id} value={row.id}>{row.title} · {row.version}</option>)}
          </select></Field>
        </>}
        {(method.quick || workspace) && <>
          {schema && parsed && typeof parsed === 'object' && <SchemaFields schema={schema} input={parsed} t={t} required={method.required_for_primary}
            setInput={(input) => { setRaw(JSON.stringify(input, null, 2)); mark(true); }} />}
          <details><summary>{t('ورودی کامل و شناسهٔ روش', 'Full input and method ID')}</summary>
            <p dir="ltr" className="technical">{method.method_id} · v{method.method_version}</p>
            <Field label={t('ورودی JSON', 'JSON input')}><textarea className="technical" dir="ltr" value={raw}
              onChange={(event) => { setRaw(event.target.value); mark(true); }} /></Field>
          </details>
          <div className="row">
            <button className="secondary" disabled={task.busy} onClick={() => submit('check')}>{t('بررسی ورودی', 'Check input')}</button>
            {canSave && <button className="primary" disabled={task.busy || !question.trim() || !!newerDraft || (!!selected && !dirty)}
              onClick={() => submit('save')}>{t('ذخیرهٔ پیش‌نویس', 'Save draft')}</button>}
          </div>
        </>}
        {!workspace && !method.quick && <Message text={t('برای ذخیرهٔ پیش‌نویس، یک کسب‌وکار انتخاب کنید.',
          'Select a workspace to save a draft.')} />}
        <details open={!!check}>
          <summary>{t('پیش‌شرط‌ها و محدودیت‌ها', 'Requirements and limitations')}</summary>
          <ul>{(check?.required_for_primary ?? method.required_for_primary).map((item) => <li key={item}>{item}</li>)}</ul>
          {check && <Message text={check.missing_fields.length
            ? t('ورودی‌های مفقود', 'Missing inputs') + ' · ' + check.missing_fields.join(' · ')
            : t('پیش‌شرط‌های ورودی بررسی شدند.', 'Input requirements checked.')} />}
          <p>{check?.limitations[0] ?? method.release_gate}</p>
        </details>
      </fieldset>}
      {base && <section className="saved">
        <h3>{t('پیش‌نویس‌های من', 'My drafts')}</h3>
        <ul className="record-list">{drafts.map((draft) => <li key={draft.id}><button className="record"
          onClick={() => choose(draft.request.tool_id, draft)}>
          <span>{draft.request.question}</span><small>{t('نسخه', 'Version')} {draft.version}</small>
        </button></li>)}</ul>
        <h3>{t('نتیجه‌های ثبت‌شده', 'Recorded results')}</h3>
        {runs.length ? <ul className="record-list">{runs.map((run) => <li key={run.run_id}><button className="record"
          onClick={() => task.run(async () => {
            setResult(run); setVersions(undefined);
            setVersions(await api<SourceVersions>(base + '/runs/' + run.run_id + '/sources'));
          })}>{title(run.tool_id, t)} · {run.status}</button></li>)}</ul>
          : <p className="muted">{t('هنوز اجرایی ثبت نشده است.', 'No runs have been recorded.')}</p>}
        {result && <div className="inset" role="region" aria-label={t('نتیجه', 'Result')}>
          <p><bdi>{result.method_id} · v{result.method_version}</bdi></p>
          <p>{result.status} · {result.analysis_status}</p>
          {versions?.stale && <Message text={t('نسخهٔ جدیدی از منبع وجود دارد.', 'A newer source version is available.')} />}
          {!!versions?.refs.length && <details>
            <summary>{t('منابع و نسخه‌ها', 'Sources and versions')}</summary>
            <ul>{versions.refs.map((ref) => <li key={ref.kind + ref.id + ref.version}>
              <bdi>{ref.kind} · {ref.id}</bdi> · {t('نسخه', 'Version')} {ref.version}
            </li>)}</ul>
          </details>}
          {result.findings.map((finding) => <p key={finding.statement}>{finding.kind} · {finding.statement}</p>)}
          {result.limitations.map((item) => <p key={item}>{item}</p>)}<p>{result.next_action}</p>
          {workspace && result.options.length > 0 && <Decisions key={result.run_id} result={result} workspace={workspace} t={t} />}
        </div>}
      </section>}
    </section>
    <Catalog methods={methods} current={tool} select={choose} t={t} />
  </div>;
}
