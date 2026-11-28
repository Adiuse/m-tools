import { useEffect, useState } from 'react';
import { api, ApiError, errorText } from './api';
import type { Ref, Translate, Workspace } from './api';
import { Field, formValues, Message, useTask } from './shared';

type Version = { id: string; version: number; series: string; created_at: string };
type Evidence = Version & {
  title: string; kind: string; source_uri: string; collected_at: string; quality_notes: string; claim_only: boolean;
};
type Profile = Version & {
  industry: string; offering: string; objective: string; geography: string; business_model: string;
  company_name: string; target_segment: string; channels: string; public_contact: string; pricing_terms: string;
  pricing_currency: string; pricing_date: string | null;
};
type SeriesRow = {
  series_key: string; period_start: string; value: number | null; unit: string;
  currency: string | null; source_ref: Ref;
};
type Dataset = Version & { title: string; row_count: number; payload: {
  schema_id: string; synthetic: boolean; source_ref: Ref; rows: SeriesRow[]; scope: {
    population: string; unit: string; grain: string; cohort: string | null; period: { start: string; end_exclusive: string; timezone: string };
  };
} };
type HistoryEvent = { id: string; action: string; created_at: string; entity_id: string };
type Member = { id: string; email: string; role: string; active: boolean };

function useList<T>(path: string, t: Translate) {
  const [items, setItems] = useState<T[]>([]);
  const [error, setError] = useState('');
  useEffect(() => {
    let current = true;
    api<T[]>(path).then((rows) => { if (current) setItems(rows); })
      .catch((cause) => { if (current) setError(errorText(cause, t)); });
    return () => { current = false; };
  }, [path, t]);
  return { items, error, add: (row: T) => setItems((previous) => [row, ...previous]) };
}

function VersionList<T extends Version>({ items, title, select, t }: {
  items: T[]; title: (item: T) => string; select: (item: T) => void; t: Translate;
}) {
  return <ul className="record-list">{items.map((item) => <li key={item.id}>
    <button className="record" onClick={() => select(item)}>
      <span>{title(item)}</span><small>{t('نسخه', 'Version')} {item.version}</small>
    </button>
  </li>)}</ul>;
}

export function Profiles({ base, editable, t }: { base: string; editable: boolean; t: Translate }) {
  const path = base + '/entities/profiles';
  const list = useList<Profile>(path, t);
  const [selected, setSelected] = useState<Profile | null>(null);
  const task = useTask(t);
  const profile = selected ?? list.items[0];
  return <div className="split">
    <section className="panel">
      <h2>{t('پروفایل کسب‌وکار', 'Business profile')}</h2>
      <Message text={list.error || task.error} error />
      {profile && <form key={profile.id} onSubmit={(event) => {
        const data = formValues(event);
        task.run(async () => {
          const result = await api<Profile>(path + '/' + profile.id, 'PATCH', { ...data, pricing_date: data.pricing_date || null });
          list.add(result); setSelected(result);
        });
      }}>
        <Field label={t('نوع فعالیت', 'Industry')}><input name="industry" defaultValue={profile.industry} required readOnly={!editable} /></Field>
        <Field label={t('محصول یا خدمت', 'Product or service')}><input name="offering" defaultValue={profile.offering} required readOnly={!editable} /></Field>
        <Field label={t('هدف یا مسئلهٔ فعلی', 'Current objective')}><textarea name="objective" defaultValue={profile.objective} required readOnly={!editable} /></Field>
        <Field label={t('مدل کسب‌وکار', 'Business model')}><input name="business_model" defaultValue={profile.business_model} readOnly={!editable} /></Field>
        <Field label={t('بازار جغرافیایی', 'Geography')}><input name="geography" defaultValue={profile.geography} readOnly={!editable} /></Field>
        <details><summary>{t('نام، کانال و مخاطب', 'Name, channels and audience')}</summary>
          {([
            ['company_name', t('نام شرکت', 'Company name')], ['target_segment', t('بخش هدف', 'Target segment')],
            ['channels', t('کانال‌ها', 'Channels')], ['public_contact', t('تماس عمومی', 'Public contact')],
            ['pricing_terms', t('شرایط قیمت‌گذاری', 'Pricing terms')],
            ['pricing_currency', t('ارز قیمت', 'Pricing currency')],
            ['pricing_date', t('تاریخ قیمت', 'Pricing date')],
          ] as const).map(([key, label]) => <Field label={label} key={key}>
            <input name={key} type={key === 'pricing_date' ? 'date' : 'text'} defaultValue={profile[key] ?? ''} readOnly={!editable} />
          </Field>)}
        </details>
        {editable && <button className="primary" disabled={task.busy || profile.id !== list.items[0]?.id}>{t('ذخیرهٔ نسخهٔ جدید', 'Save new version')}</button>}
      </form>}
    </section>
    <aside className="panel"><h2>{t('نسخه‌ها', 'Versions')}</h2>
      <VersionList items={list.items} title={(item) => item.industry} select={setSelected} t={t} />
    </aside>
  </div>;
}

export function EvidenceRecords({ base, editable, t }: { base: string; editable: boolean; t: Translate }) {
  const path = base + '/entities/evidence';
  const list = useList<Evidence>(path, t);
  const [selected, setSelected] = useState<Evidence | null>(null);
  const task = useTask(t);
  const current = selected && !list.items.some((row) => row.series === selected.series && row.version > selected.version);
  return <div className="split">
    <section className="panel">
      <h2>{selected ? selected.title : t('ثبت شاهد', 'Record evidence')}</h2>
      {selected?.claim_only && <p className="status-tag">{t('اظهار منبع', 'Source claim')}</p>}
      <Message text={list.error || task.error} error />
      {(editable || selected) && <form key={selected?.id ?? 'new'} onSubmit={(event) => {
        const data = formValues(event);
        task.run(async () => {
          const result = await api<Evidence>(selected ? path + '/' + selected.id : path, selected ? 'PATCH' : 'POST', data);
          list.add(result); setSelected(result);
        });
      }}>
        <Field label={t('عنوان شاهد', 'Evidence title')}><input name="title" defaultValue={selected?.title} maxLength={200} required readOnly={!editable} /></Field>
        <Field label={t('نوع شاهد', 'Evidence type')}><select name="kind" defaultValue={selected?.kind || 'internal'} disabled={!editable}>
          <option value="internal">{t('داخلی', 'Internal')}</option><option value="primary">{t('دست اول', 'Primary')}</option>
          <option value="secondary">{t('ثانویه', 'Secondary')}</option><option value="assumption">{t('فرض', 'Assumption')}</option>
        </select></Field>
        <Field label={t('تاریخ گردآوری', 'Date collected')}><input type="date" name="collected_at" defaultValue={selected?.collected_at} required readOnly={!editable} /></Field>
        <Field label={t('نشانی منبع', 'Source URL')}><input name="source_uri" type="url" defaultValue={selected?.source_uri} readOnly={!editable} dir="ltr" /></Field>
        <Field label={t('یادداشت کیفیت', 'Quality notes')}><textarea name="quality_notes" defaultValue={selected?.quality_notes} readOnly={!editable} maxLength={2000} /></Field>
        {editable && <button className="primary" disabled={task.busy || (!!selected && !current)}>
          {selected ? t('ذخیرهٔ نسخهٔ جدید', 'Save new version') : t('ذخیرهٔ شاهد', 'Save evidence')}
        </button>}
      </form>}
    </section>
    <aside className="panel">
      <div className="section-head"><h2>{t('شواهد و نسخه‌ها', 'Evidence and versions')}</h2>
        {editable && <button className="link" onClick={() => setSelected(null)}>{t('شاهد جدید', 'New evidence')}</button>}
      </div>
      <VersionList items={list.items} title={(item) => item.title} select={setSelected} t={t} />
    </aside>
  </div>;
}

type EditRow = { key: string; date: string; value: string };
const emptyRow = (): EditRow => ({ key: crypto.randomUUID(), date: '', value: '' });

export function Datasets({ workspace, base, editable, t }: {
  workspace: Workspace; base: string; editable: boolean; t: Translate;
}) {
  const path = base + '/datasets';
  const list = useList<Dataset>(path, t);
  const sources = useList<Evidence>(base + '/entities/evidence', t);
  const [selected, setSelected] = useState<Dataset | null>(null);
  const [rows, setRows] = useState<EditRow[]>([emptyRow()]);
  const task = useTask(t);
  const scope = selected?.payload.scope;
  const edit = editable && (!selected || (selected.payload.schema_id === 'numeric_series' && selected.payload.scope.grain === 'day'
    && selected.payload.rows.every((row) => row.series_key === 'manual' && row.currency === null
      && row.source_ref.id === selected.payload.source_ref.id)));
  const current = selected && !list.items.some((row) => row.series === selected.series && row.version > selected.version);

  function select(item: Dataset | null) {
    setSelected(item);
    setRows(item?.payload.schema_id === 'numeric_series' && item.payload.rows.length
      ? item.payload.rows.map((row) => ({ key: crypto.randomUUID(), date: row.period_start, value: String(row.value ?? '') }))
      : [emptyRow()]);
  }

  return <div className="split">
    <section className="panel">
      <h2>{selected ? selected.title : t('ثبت سری عددی', 'Record a numeric series')}</h2>
      <Message text={list.error || sources.error || task.error} error />
      {selected?.payload.synthetic && <p className="status-tag">{t('دادهٔ مصنوعی', 'Synthetic dataset')}</p>}
      {!edit && selected && <pre className="technical" dir="ltr">{JSON.stringify(selected.payload, null, 2)}</pre>}
      {edit && <form key={selected?.id ?? 'new'} onSubmit={(event) => {
        const data = formValues(event);
        task.run(async () => {
          const evidence = sources.items.find((source) => source.id === data.evidence_id);
          if (!evidence) return;
          const source_ref = { kind: 'evidence', id: evidence.id, version: evidence.version };
          const validated = rows.map((row) => ({
            series_key: 'manual', period_start: row.date, value: row.value === '' ? null : Number(row.value),
            unit: data.unit, currency: null, source_ref,
          }));
          if (validated.some((row) => row.value !== null && !Number.isFinite(row.value))) {
            throw new ApiError(422, { field: t("مقدار", "Value") });
          }
          const payload = {
            ...selected?.payload, schema_id: 'numeric_series', schema_version: 1, workspace_id: workspace.id, source_ref,
            scope: { ...scope, population: data.population, grain: 'day', period: {
              start: data.start, end_exclusive: data.end, timezone: scope?.period.timezone ?? workspace.timezone,
            }, cohort: scope?.cohort ?? null, unit: data.unit },
            rows: validated,
            ...(selected ? {} : { columns: [], coverage: 'unknown' }),
            synthetic: selected?.payload.synthetic ?? (data.synthetic === 'on'),
          };
          const result = await api<Dataset>(selected ? base + '/entities/datasets/' + selected.id : path,
            selected ? 'PATCH' : 'POST', { title: data.title, payload });
          list.add(result); select(result);
        });
      }}>
        {!selected && <Field label={t('دادهٔ مصنوعی', 'Synthetic dataset')}><input type="checkbox" name="synthetic" /></Field>}
        <Field label={t('عنوان مجموعه‌داده', 'Dataset title')}><input name="title" defaultValue={selected?.title} maxLength={200} required /></Field>
        <Field label={t('شاهد مبنا', 'Source evidence')}><select name="evidence_id" required defaultValue={selected?.payload.source_ref.id ?? ''}>
          <option value="" disabled>{t('شاهد را انتخاب کنید', 'Select evidence')}</option>
          {sources.items.filter((source) => source.kind !== 'assumption').map((source) =>
            <option key={source.id} value={source.id}>{source.title} · {source.version}{source.claim_only ? ' · ' + t('اظهار منبع', 'Source claim') : ''}</option>)}
        </select></Field>
        <div className="form-grid">
          <Field label={t('جامعه یا دامنه', 'Population or scope')}><input name="population" defaultValue={scope?.population} required /></Field>
          <Field label={t('واحد', 'Unit')}><input name="unit" defaultValue={scope?.unit} required /></Field>
          <Field label={t('شروع بازه', 'Period start')}><input type="date" name="start" defaultValue={scope?.period.start} required /></Field>
          <Field label={t('پایان بازه، غیرشامل', 'Exclusive period end')}><input type="date" name="end" defaultValue={scope?.period.end_exclusive} required /></Field>
        </div>
        {rows.map((row, index) => <div className="row inputs" key={row.key}>
          <Field label={t('تاریخ ردیف', 'Row date') + ' ' + (index + 1)}><input type="date" value={row.date} required onChange={(event) =>
            setRows((previous) => previous.map((item) => item.key === row.key ? { ...item, date: event.target.value } : item))} /></Field>
          <Field label={t('مقدار', 'Value') + ' ' + (index + 1)}><input type="number" step="any" value={row.value} onChange={(event) =>
            setRows((previous) => previous.map((item) => item.key === row.key ? { ...item, value: event.target.value } : item))} /></Field>
          {rows.length > 1 && <button type="button" className="link" onClick={() => setRows((previous) => previous.filter((item) => item.key !== row.key))}>{t('حذف ردیف', 'Remove row')}</button>}
        </div>)}
        <div className="row">
          <button type="button" className="secondary" onClick={() => setRows((previous) => [...previous, emptyRow()])}>{t('افزودن ردیف', 'Add row')}</button>
          <button className="primary" disabled={task.busy || (!!selected && !current)}>{selected ? t('ذخیرهٔ نسخهٔ جدید', 'Save new version') : t('ذخیرهٔ داده', 'Save dataset')}</button>
        </div>
      </form>}
    </section>
    <aside className="panel">
      <div className="section-head"><h2>{t('داده‌ها و نسخه‌ها', 'Datasets and versions')}</h2>
        {editable && <button className="link" onClick={() => select(null)}>{t('دادهٔ جدید', 'New dataset')}</button>}
      </div>
      <VersionList items={list.items} title={(item) => item.title + (item.payload.synthetic ? ' · ' + t('مصنوعی', 'Synthetic') : '')} select={select} t={t} />
    </aside>
  </div>;
}

export function History({ base, t }: { base: string; t: Translate }) {
  const list = useList<HistoryEvent>(base + '/history', t);
  const titles: Record<string, string> = {
    workspace_created: t('ایجاد کسب‌وکار', 'Workspace created'),
    evidence_created: t('ثبت شاهد', 'Evidence recorded'),
    evidence_revised: t('نسخهٔ جدید شاهد', 'Evidence revised'),
    datasets_created: t('ثبت داده', 'Dataset recorded'),
    datasets_revised: t('نسخهٔ جدید داده', 'Dataset revised'),
    profiles_revised: t('ویرایش پروفایل', 'Profile revised'),
    membership_updated: t('تغییر دسترسی عضو', 'Membership updated'),
  };
  return <section className="panel">
    <h2>{t('تاریخچهٔ کسب‌وکار', 'Workspace history')}</h2><Message error text={list.error} />
    <ul className="record-list">{list.items.map((item) => <li className="history-row" key={item.id}>
      <span>{titles[item.action] ?? item.action}</span>
      <time dateTime={item.created_at}>{new Date(item.created_at).toLocaleString(t('fa-IR', 'en-US'))}</time>
    </li>)}</ul>
  </section>;
}

export function Members({ base, t }: { base: string; t: Translate }) {
  const path = base + '/memberships';
  const list = useList<Member>(path, t);
  const task = useTask(t);
  return <div className="split">
    <form className="panel" onSubmit={(event) => {
      const values = formValues(event);
      task.run(async () => list.add(await api<Member>(path, 'POST', { ...values, active: values.active === 'true' })));
    }}>
      <h2>{t('دسترسی اعضا', 'Member access')}</h2>
      <Field label={t('ایمیل حساب فعال', 'Active account email')}><input type="email" name="email" required dir="ltr" /></Field>
      <Field label={t('نقش', 'Role')}><select name="role"><option value="viewer">{t('خواننده', 'Viewer')}</option>
        <option value="editor">{t('ویرایشگر', 'Editor')}</option><option value="owner">{t('مالک', 'Owner')}</option></select></Field>
      <Field label={t('وضعیت', 'Status')}><select name="active"><option value="true">{t('فعال', 'Active')}</option>
        <option value="false">{t('غیرفعال', 'Inactive')}</option></select></Field>
      <Message error text={task.error || list.error} />
      <button className="primary" disabled={task.busy}>{t('ثبت دسترسی', 'Save access')}</button>
    </form>
    <section className="panel"><h2>{t('اعضا', 'Members')}</h2><ul className="record-list">
      {list.items.filter((row, index, all) => all.findIndex((entry) => entry.id === row.id) === index)
        .map((row) => <li className="history-row" key={row.id}><bdi>{row.email}</bdi><span>{row.active ? row.role : t('غیرفعال', 'Inactive')}</span></li>)}
    </ul></section>
  </div>;
}
