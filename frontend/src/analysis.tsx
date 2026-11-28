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

type JSONProperty = { type?: string; enum?: string[]; anyOf?: JSONProperty[]; $ref?: string };
type InputSchema = { $ref: string; $defs: Record<string, { properties?: Record<string, JSONProperty> }> };
type ToolDetail = { methods: Method[]; schemas: Record<string, InputSchema> };
type Preflight = { availability: string; required_for_primary: string[]; limitations: string[] };
type Result = { run_id: string; tool_id: string; status: string; analysis_status: string | null;
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
    .filter((method) => (catalogId(method) + ' ' + title(catalogId(method), t)).toLowerCase().includes(query.toLowerCase()));
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
        <small>{t('برنامه‌ریزی‌شده', 'Planned')}</small>
      </button></li>)}</ul>
  </section>;
}

function SchemaFields({ schema, input, setInput, t }: {
  schema: InputSchema; input: Record<string, unknown>; setInput: (data: Record<string, unknown>) => void; t: Translate;
}) {
  const properties = schema.$defs[schema.$ref.split('/').at(-1) ?? '']?.properties ?? {};
  function update(key: string, value: string) {
    const next = { ...input };
    if (value === '') delete next[key];
    else if (properties[key].type === 'number' || properties[key].type === 'integer') next[key] = Number(value);
    else next[key] = value;
    setInput(next);
  }
  return <>
    {Object.entries(properties).filter(([, spec]) => ['string', 'number', 'integer'].includes(spec.type ?? '') || spec.enum).map(([key, spec]) =>
      <Field key={key} label={key.replaceAll('_', ' ')}>{spec.enum
        ? <select value={String(input[key] ?? '')} onChange={(event) => update(key, event.target.value)}>
          <option value="">{t('انتخاب کنید', 'Select')}</option>
          {spec.enum.map((option) => <option key={option}>{option}</option>)}
        </select>
        : <input type={spec.type === 'number' || spec.type === 'integer' ? 'number' : 'text'}
          step={spec.type === 'number' ? 'any' : undefined} value={String(input[key] ?? '')} onChange={(event) => update(key, event.target.value)} />}</Field>)}
  </>;
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

export function AnalysisPage({ workspace, methods, t, onDirty }: {
  workspace?: Workspace; methods: Method[]; t: Translate; onDirty: (dirty: boolean) => void;
}) {
  const base = workspace ? '/workspaces/' + workspace.id : '';
  const [tool, setTool] = useState('');
  const [methodId, setMethod] = useState('');
  const [detail, setDetail] = useState<ToolDetail>();
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [selected, setSelected] = useState<Draft>();
  const [evidence, setEvidence] = useState<EvidenceChoice[]>([]);
  const [source, setSource] = useState('');
  const [runs, setRuns] = useState<Result[]>([]);
  const [result, setResult] = useState<Result>();
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
    if (!base) return;
    let current = true;
    Promise.all([api<Draft[]>(base + '/drafts'), api<EvidenceChoice[]>(base + '/entities/evidence'), api<Result[]>(base + '/runs')])
      .then(([draftRows, evidenceRows, runRows]) => {
        if (current) { setDrafts(draftRows); setEvidence(evidenceRows); setRuns(runRows); }
      }).catch((error) => { if (current) setLoadError(errorText(error, t)); });
    return () => { current = false; };
  }, [base, t]);

  function mark(changed: boolean) {
    setDirty(changed);
    if (canSave) onDirty(changed);
    if (changed) { setCheck(undefined); setNotice(''); setRequestKey(crypto.randomUUID()); }
  }

  function choose(id: string, draft?: Draft) {
    if (dirty && !window.confirm(t('تغییرات ذخیره نشده‌اند. ادامه می‌دهید؟', 'Discard unsaved changes?'))) return;
    setDetail(undefined); setTool(id); setMethod(draft?.request.method_id ?? '');
    setSelected(draft); setQuestion(draft?.request.question ?? '');
    setSource(draft?.request.evidence_refs[0]?.id ?? '');
    setRaw(JSON.stringify(draft?.request.input ?? {}, null, 2)); setResult(undefined);
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
      const selectedEvidence = evidence.find((row) => row.id === source);
      const refs: Ref[] = selectedEvidence ? [{ kind: 'evidence', id: source, version: selectedEvidence.version }] : [];
      const body: RunRequest = {
        workspace_id: workspace.id, tool_id: method.tool_id, method_id: method.method_id,
        method_version: method.method_version, question, input, evidence_refs: refs,
        dependency_run_ids: [], idempotency_key: requestKey,
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
      {method && <>
        {detail && detail.methods.length > 1 && <Field label={t('روش', 'Method')}><select value={method.method_id}
          onChange={(event) => { setMethod(event.target.value); setRaw('{}'); mark(true); }}>
          {detail.methods.map((item) => <option key={item.method_id} value={item.method_id}>{item.method_id} · v{item.method_version}</option>)}
        </select></Field>}
        <p className="status-tag">{t('برنامه‌ریزی‌شده', 'Planned')}</p>
        {!method.quick && workspace && <>
          <Field label={t('سؤال تحلیل', 'Analysis question')}><textarea value={question} maxLength={1200}
            onChange={(event) => { setQuestion(event.target.value); mark(true); }} /></Field>
          <Field label={t('شاهد', 'Evidence')}><select value={source} onChange={(event) => { setSource(event.target.value); mark(true); }}>
            <option value="">{t('انتخاب نشده', 'None selected')}</option>
            {evidence.map((row) => <option key={row.id} value={row.id}>{row.title} · {row.version}</option>)}
          </select></Field>
        </>}
        {(method.quick || workspace) && <>
          {schema && parsed && typeof parsed === 'object' && <SchemaFields schema={schema} input={parsed} t={t}
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
          <p>{check?.limitations[0] ?? method.release_gate}</p>
        </details>
      </>}
      {base && <section className="saved">
        <h3>{t('پیش‌نویس‌های من', 'My drafts')}</h3>
        <ul className="record-list">{drafts.map((draft) => <li key={draft.id}><button className="record"
          onClick={() => choose(draft.request.tool_id, draft)}>
          <span>{draft.request.question}</span><small>{t('نسخه', 'Version')} {draft.version}</small>
        </button></li>)}</ul>
        <h3>{t('نتیجه‌های ثبت‌شده', 'Recorded results')}</h3>
        {runs.length ? <ul className="record-list">{runs.map((run) => <li key={run.run_id}><button className="record"
          onClick={() => setResult(run)}>{title(run.tool_id, t)} · {run.status}</button></li>)}</ul>
          : <p className="muted">{t('هنوز اجرایی ثبت نشده است.', 'No runs have been recorded.')}</p>}
        {result && <div className="inset" role="region" aria-label={t('نتیجه', 'Result')}>
          <p>{result.status} · {result.analysis_status}</p>
          {result.findings.map((finding) => <p key={finding.statement}>{finding.kind} · {finding.statement}</p>)}
          {result.limitations.map((item) => <p key={item}>{item}</p>)}<p>{result.next_action}</p>
          {workspace && result.options.length > 0 && <Decisions key={result.run_id} result={result} workspace={workspace} t={t} />}
        </div>}
      </section>}
    </section>
    <Catalog methods={methods} current={tool} select={choose} t={t} />
  </div>;
}
