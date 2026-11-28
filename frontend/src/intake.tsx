import { useEffect, useState } from 'react';
import { api, errorText } from './api';
import type { Translate, Workspace } from './api';
import { Field, formValues, Message, useTask } from './shared';

type Evidence = { id: string; title: string; version: number; kind: string; claim_only: boolean };
type ReportSource = { id: string; title: string; version: number; synthetic: boolean; artifact_type: string };
type Props = { workspace: Workspace; t: Translate };

function useRows<T>(path: string, t: Translate) {
  const [records, setRecords] = useState<T[]>([]);
  const [error, setError] = useState('');
  useEffect(() => {
    let mounted = true;
    api<T[]>(path).then((items) => { if (mounted) setRecords(items); })
      .catch((cause) => { if (mounted) setError(errorText(cause, t)); });
    return () => { mounted = false; };
  }, [path, t]);
  return { records, error };
}

type Preview = {
  id: string; checksum: string; accepted: number; synthetic: boolean;
  template_version: number; mapping: Record<string, string>;
  errors: { row: number; reason: string }[]; rows: Record<string, unknown>[];
};

export function FileIntake({ workspace, t }: Props) {
  const base = '/workspaces/' + workspace.id;
  const evidence = useRows<Evidence>(base + '/entities/evidence', t);
  const schemas = useRows<{ schema_id: string; columns: string[] }>('/dataset-templates', t);
  const [schema, setSchema] = useState('numeric_series');
  const [staged, setStaged] = useState<Preview>();
  const [title, setTitle] = useState('');
  const [saved, setSaved] = useState(false);
  const task = useTask(t);
  const template = '/api/dataset-templates?schema_id=' + schema + '&locale=' + t('fa', 'en');
  return <div className="split">
    <form className="panel" onSubmit={(event) => {
      event.preventDefault();
      const body = new FormData(event.currentTarget);
      const selected = evidence.records.find((item) => item.id === body.get('evidence'));
      if (!selected) return;
      const metadata = {
        schema_id: schema, source_ref: { id: selected.id, version: selected.version, kind: 'evidence' },
        synthetic: body.has('synthetic'), coverage: 'unknown', columns: [],
        scope: { population: body.get('population'), grain: body.get('grain'), unit: body.get('unit'), cohort: null,
          period: { start: body.get('start'), end_exclusive: body.get('end'), timezone: workspace.timezone } },
      };
      body.set('metadata', JSON.stringify(metadata));
      setSaved(false);
      setStaged(undefined);
      task.run(async () => setStaged(await api<Preview>(base + '/datasets/previews', 'POST', body)));
    }}>
      <h2>{t('ورود داده از فایل', 'Import tabular data')}</h2>
      <Field label={t('ساختار داده', 'Dataset schema')}><select value={schema} onChange={(event) => setSchema(event.target.value)}>
        {schemas.records.map((item) => <option key={item.schema_id}>{item.schema_id}</option>)}
      </select></Field>
      <div className="row">
        <a href={template}>{t('قالب CSV', 'CSV template')}</a>
        <a href={template + '&file_format=xlsx'}>{t('قالب Excel', 'Excel template')}</a>
        {schema === 'numeric_series' && <a href={template + '&example=1'}>{t('دانلود مثال مصنوعی', 'Download synthetic example')}</a>}
      </div>
      <p className="technical">{schemas.records.find((item) => item.schema_id === schema)?.columns.join(' · ')}</p>
      <Field label={t('فایل CSV یا Excel', 'CSV or Excel file')}><input type="file" name="file" accept=".csv,.xlsx" required /></Field>
      <div className="form-grid">
        <Field label={t('نام برگهٔ Excel', 'Excel sheet name')}><input name="sheet" /></Field>
        <Field label={t('جداکنندهٔ CSV', 'CSV delimiter')}><select name="delimiter"><option value=",">,</option><option value=";">;</option><option value={'\t'}>Tab</option></select></Field>
        <Field label={t('شاهد مبنا', 'Source evidence')}><select name="evidence" required defaultValue="">
          <option value="" disabled>{t('انتخاب کنید', 'Select')}</option>
          {evidence.records.map((item) => <option key={item.id} value={item.id}>{item.title} · {item.version}{item.claim_only ? ' · ' + t('اظهار منبع', 'Source claim') : ''}</option>)}
        </select></Field>
        <Field label={t('جامعه یا دامنه', 'Population or scope')}><input name="population" required /></Field>
        <Field label={t('دانه‌بندی', 'Grain')}><input name="grain" defaultValue="day" required /></Field>
        <Field label={t('واحد', 'Unit')}><input name="unit" required /></Field>
        <Field label={t('شروع بازه', 'Period start')}><input type="date" name="start" required /></Field>
        <Field label={t('پایان بازه، غیرشامل', 'Exclusive period end')}><input type="date" name="end" required /></Field>
      </div>
      <Field label={t('نگاشت ستون‌های سفارشی (JSON)', 'Custom column mapping (JSON)')}><textarea name="mapping" defaultValue="{}" dir="ltr" /></Field>
      <Field label={t('دادهٔ مصنوعی', 'Synthetic dataset')}><input type="checkbox" name="synthetic" /></Field>
      <button className="primary" disabled={task.busy}>{t('پیش‌نمایش فایل', 'Preview file')}</button>
      <Message text={task.error || evidence.error || schemas.error} error />
    </form>
    {staged && <section className="panel">
      <h2>{t('بازبینی ردیف‌ها', 'Review rows')}</h2>
      <p>{t('معتبر', 'Valid')} {staged.accepted} · {t('دارای خطا', 'Errors')} {staged.errors.length}</p>
      {staged.synthetic && <p className="status-tag">{t('مصنوعی', 'Synthetic')}</p>}
      {staged.errors.length > 0 && <>
        <a href={'/api' + base + '/datasets/previews/' + staged.id + '/errors'}>{t('دانلود خطاها', 'Download errors')}</a>
        <ul>{staged.errors.slice(0, 8).map((item) => <li key={item.row}>{item.row} · {item.reason}</li>)}</ul>
      </>}
      <pre className="technical" dir="ltr">{JSON.stringify(staged.rows.slice(0, 3), null, 2)}</pre>
      <form onSubmit={(event) => {
        event.preventDefault();
        task.run(async () => {
          await api(base + '/datasets', 'POST', { preview_id: staged.id, checksum: staged.checksum, title,
            mapping: staged.mapping, template_version: staged.template_version, confirm: true });
          setSaved(true);
        });
      }}>
        <Field label={t('عنوان مجموعه‌داده', 'Dataset title')}><input value={title} onChange={(event) => setTitle(event.target.value)} maxLength={200} required /></Field>
        <button className="primary" disabled={task.busy || saved || !!staged.errors.length || !staged.accepted}>
          {t('تأیید و ثبت داده', 'Confirm and save dataset')}
        </button>
      </form>
      <Message text={saved ? t('نسخهٔ داده ذخیره شد.', 'Dataset version saved.') : ''} />
    </section>}
  </div>;
}

type ProfilePreview = { id: string; checksum: string; base_version: number; missing_fields: string[];
  ambiguous_fields?: string[]; fields: { field: string; current: string; proposed: string; anchor: string; conflict: boolean }[] };

export function ProfileIntake({ workspace, t }: Props) {
  const base = '/workspaces/' + workspace.id + '/intakes/previews';
  const [review, setReview] = useState<ProfilePreview>();
  const [saved, setSaved] = useState(false);
  const task = useTask(t);
  return <div className="split">
    <form className="panel" onSubmit={(event) => {
      event.preventDefault();
      const body = new FormData(event.currentTarget);
      setReview(undefined); setSaved(false);
      task.run(async () => setReview(await api<ProfilePreview>(base, 'POST', body)));
    }}>
      <h2>{t('تکمیل پروفایل از منبع', 'Review a profile source')}</h2>
      <Field label={t('نشانی عمومی HTTPS', 'Public HTTPS URL')}><input type="url" name="url" dir="ltr" /></Field>
      <Field label={t('فایل سند', 'Source document')}><input type="file" name="file" accept=".txt,.pdf,.docx,.xlsx,.pptx,.csv" /></Field>
      <Field label={t('اجازهٔ استفاده از این منبع را دارم', 'I have permission to use this source')}><input type="checkbox" name="authorized" value="yes" required /></Field>
      <button className="primary" disabled={task.busy}>{t('بازبینی منبع', 'Review source')}</button>
      <Message text={task.error} error />
    </form>
    {review && <form className="panel" key={review.id} onSubmit={(event) => {
      const values = formValues(event);
      const selected = Object.fromEntries(review.fields.filter((item) => values['accept-' + item.field])
        .map((item) => [item.field, values[item.field]]));
      task.run(async () => {
        await api(base + '/' + review.id + '/apply', 'POST', { fields: selected, checksum: review.checksum,
          expected_version: review.base_version, confirm: true });
        setSaved(true);
      });
    }}>
      <h2>{t('موارد پیشنهادی', 'Suggested fields')}</h2>
      {review.fields.map((item) => <div key={item.field} className="inset">
        <p>{item.field} · {item.anchor} · {t('اظهار منبع', 'Source claim')}</p>
        {item.conflict && <p>{t('مقدار منبع با اطلاعات ثبت‌شده متفاوت است.', 'The source differs from the saved value.')}</p>}
        <p>{t('مقدار فعلی', 'Current value')} · {item.current}</p>
        <Field label={t('مقدار پیشنهادی', 'Proposed value') + ' · ' + item.field}><input name={item.field} defaultValue={item.proposed} /></Field>
        <Field label={t('انتخاب فیلد', 'Select field') + ' · ' + item.field}><input type="checkbox" name={'accept-' + item.field} /></Field>
      </div>)}
      <p>{t('در انتظار شاهد', 'Pending evidence')} · {review.missing_fields.join(' · ')}</p>
      {!!review.ambiguous_fields?.length && <p>{t('مقادیر متعارض در منبع', 'Conflicting values in the source')} · {review.ambiguous_fields.join(' · ')}</p>}
      <button className="primary" disabled={task.busy || saved || !review.fields.length}>{t('تأیید نسخهٔ جدید', 'Confirm new profile version')}</button>
      <Message text={saved ? t('نسخهٔ پروفایل ذخیره شد.', 'Profile version saved.') : ''} />
    </form>}
  </div>;
}

type Export = { id: string; state: string; format: string; stale: boolean; snapshot: { checksum: string; status: string; title: string } };

export function Exports({ workspace, t }: Props) {
  const base = '/workspaces/' + workspace.id;
  const datasets = useRows<ReportSource>(base + '/exports/sources', t);
  const earlier = useRows<Export>(base + '/exports', t);
  const [report, setReport] = useState<Export>();
  const [error, setError] = useState('');
  const task = useTask(t);
  const runningId = report && ['queued', 'running'].includes(report.state) ? report.id : undefined;
  useEffect(() => {
    if (!runningId) return;
    const timer = setInterval(() => {
      api<Export>(base + '/exports/' + runningId).then(setReport)
        .catch((cause) => { clearInterval(timer); setError(errorText(cause, t)); });
    }, 1200);
    return () => clearInterval(timer);
  }, [base, runningId, t]);
  return <section className="panel">
    <h2>{t('گزارش مدیریتی', 'Executive report')}</h2>
    <form onSubmit={(event) => {
      const data = formValues(event);
      const source = datasets.records.find((item) => item.id === data.id);
      if (!source) return;
      setError('');
      task.run(async () => setReport(await api<Export>(base + '/exports', 'POST', { ...data, version: source.version, artifact_type: source.artifact_type })));
    }}>
      <Field label={t('نسخهٔ داده یا گزارش', 'Data or report version')}><select name="id" required defaultValue="">
        <option value="" disabled>{t('انتخاب کنید', 'Select')}</option>
        {datasets.records.map((item) => <option key={item.id} value={item.id}>
          {item.title} · {item.version}{item.synthetic ? ' · ' + t('مصنوعی', 'Synthetic') : ''}
        </option>)}
      </select></Field>
      <div className="form-grid">
        <Field label={t('فرمت', 'Format')}><select name="format">{['pdf', 'docx', 'xlsx', 'pptx'].map((item) =>
          <option key={item} value={item}>{item.toUpperCase()}</option>)}</select></Field>
        <Field label={t('الگوی گزارش', 'Report template')}><select name="template">
          <option value="executive">{t('مدیریتی', 'Executive')}</option><option value="detailed">{t('تفصیلی', 'Detailed')}</option></select></Field>
        <Field label={t('زبان گزارش', 'Report language')}><select name="locale" defaultValue={t('fa', 'en')}>
          <option value="fa">فارسی</option><option value="en">English</option></select></Field>
      </div>
      <button className="primary" disabled={task.busy || !!runningId}>{t('ساخت گزارش', 'Create report')}</button>
    </form>
    <Message text={error || task.error || datasets.error} error />
    {report && <p role="status">{report.snapshot.title} · {report.snapshot.status} · {report.state}
      {report.stale && ' · ' + t('نسخهٔ تازهٔ منبع موجود است', 'Newer source version available')}</p>}
    {report?.state === 'succeeded' && <a href={'/api' + base + '/exports/' + report.id + '/download'}>
      {t('دانلود گزارش', 'Download report')}</a>}
    {earlier.records.length > 0 && <ul className="record-list">{earlier.records.map((item) =>
      <li key={item.id}><button className="record" onClick={() => task.run(async () =>
        setReport(await api<Export>(base + '/exports/' + item.id)))}>
        {item.snapshot.title} · {item.format.toUpperCase()} · {item.state}
      </button></li>)}</ul>}
  </section>;
}
