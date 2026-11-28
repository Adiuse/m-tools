import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { api, errorText } from './api';
import type { Method, Translate, User, Workspace } from './api';
import { AnalysisPage } from './analysis';
import { Datasets, EvidenceRecords, History, Members, Profiles } from './records';
import { SessionForm } from './session';
import type { AccountLink } from './session';
import { Field, formValues, Message, useTask } from './shared';
import './style.css';

const fa: Translate = (value) => value;
const en: Translate = (_, value) => value;

function readAccountLink(): AccountLink | null {
  const params = new URLSearchParams(location.hash.slice(1));
  const mode = params.get('mode'), uid = params.get('uid'), token = params.get('token');
  if ((mode === 'activate' || mode === 'reset') && uid && token) {
    history.replaceState(null, '', location.pathname);
    return { mode, uid, token };
  }
  return null;
}

function WorkspaceForm({ t, onSave, onCancel }: {
  t: Translate; onSave: (workspace: Workspace) => void; onCancel: () => void;
}) {
  const task = useTask(t);
  return <form className="panel workspace-form" onSubmit={(event) => {
    const data = formValues(event);
    task.run(async () => onSave(await api<Workspace>('/workspaces', 'POST', data)));
  }}>
    <h2>{t('کسب‌وکار جدید', 'New workspace')}</h2>
    <div className="form-grid">
      <Field label={t('نام کسب‌وکار', 'Workspace name')}><input name="name" maxLength={160} required autoFocus /></Field>
      <Field label={t('نوع فعالیت', 'Industry')}><input name="industry" maxLength={160} required /></Field>
      <Field label={t('محصول یا خدمت', 'Product or service')}><input name="offering" maxLength={200} required /></Field>
      <Field label={t('هدف یا مسئلهٔ فعلی', 'Current objective')}><input name="objective" maxLength={400} required /></Field>
      <Field label={t('کد ارز', 'Currency code')}><input name="currency" pattern="[A-Z]{3}" maxLength={3} placeholder="EUR" dir="ltr" required /></Field>
      <Field label={t('منطقهٔ زمانی', 'Timezone')}><input name="timezone" dir="ltr" defaultValue={Intl.DateTimeFormat().resolvedOptions().timeZone} required /></Field>
    </div>
    <Message error text={task.error} />
    <div className="row"><button className="primary" disabled={task.busy}>{t('ایجاد کسب‌وکار', 'Create workspace')}</button>
      <button className="link" type="button" onClick={onCancel}>{t('بازگشت', 'Back')}</button></div>
  </form>;
}

type Page = 'desk' | 'catalog' | 'create' | 'profile' | 'evidence' | 'datasets' | 'analysis' | 'history' | 'members';

function App() {
  const [lang, setLang] = useState(() => localStorage.getItem('mtools-language') === 'en' ? 'en' : 'fa');
  const [user, setUser] = useState<User | null | undefined>();
  const [space, setSpace] = useState<Workspace>();
  const [spaces, setSpaces] = useState<Workspace[]>([]);
  const [methods, setMethods] = useState<Method[]>([]);
  const [page, setPage] = useState<Page>('desk');
  const [error, setError] = useState('');
  const [dirty, setDirty] = useState(false);
  const [link] = useState(readAccountLink);
  const t = lang === 'fa' ? fa : en;

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'fa' ? 'rtl' : 'ltr';
    localStorage.setItem('mtools-language', lang);
  }, [lang]);

  useEffect(() => {
    api<{ user: User | null }>('/me').then((state) => setUser(state.user))
      .catch((cause) => setError(errorText(cause, t)));
  }, [t]);

  useEffect(() => {
    if (!user) return;
    Promise.all([api<Workspace[]>('/workspaces'), api<Method[]>('/tools')])
      .then(([workspaces, catalog]) => { setSpaces(workspaces); setMethods(catalog); })
      .catch((cause) => setError(errorText(cause, t)));
  }, [user, t]);

  useEffect(() => {
    if (!dirty) return;
    function confirmLeave(event: BeforeUnloadEvent) {
      event.preventDefault();
    }
    window.addEventListener('beforeunload', confirmLeave);
    return () => window.removeEventListener('beforeunload', confirmLeave);
  }, [dirty]);

  function open(next?: Workspace, nextPage: Page = 'desk') {
    if (space?.id !== next?.id && dirty && !window.confirm(t('پیش‌نویس ذخیره نشده است. خارج می‌شوید؟',
      'Leave this workspace with an unsaved draft?'))) return;
    if (space?.id !== next?.id) setDirty(false);
    setSpace(next); setPage(nextPage); setError('');
  }

  const locale = <button type="button" className="locale" lang={lang === 'fa' ? 'en' : 'fa'}
    onClick={() => setLang(lang === 'fa' ? 'en' : 'fa')}>{lang === 'fa' ? 'English' : 'فارسی'}</button>;
  if (!user) return <><header className="topbar standalone">{locale}</header>
    <Message text={error} error />
    {user === null && <SessionForm t={t} link={link} onLogin={setUser} />}
  </>;

  const navigation: [Page, string][] = space ? [
    ['profile', t('پروفایل', 'Profile')], ['evidence', t('شواهد', 'Evidence')], ['datasets', t('داده‌ها', 'Datasets')],
    ['analysis', t('تحلیل و پیش‌نویس‌ها', 'Analysis and drafts')], ['history', t('تاریخچه', 'History')],
    ...(space.role === 'owner' ? [['members', t('اعضا', 'Members')] as [Page, string]] : []),
  ] : [['desk', t('میزکار من', 'My workbench')], ['catalog', t('کاتالوگ ابزارها', 'Tool catalog')]];
  const base = space ? '/workspaces/' + space.id : '';
  const editable = space?.role !== 'viewer';

  return <div className="shell">
    <a href="#content" className="skip">{t('رفتن به محتوا', 'Skip to content')}</a>
    <aside className="sidebar">
      <button className="wordmark" onClick={() => open()}>M<span>·</span>TOOLS</button>
      {space && <div className="sidebar-context"><strong>{space.name}</strong>
        <small>{t('فضای کاری', 'Workspace')}</small></div>}
      <nav aria-label={t('ناوبری میزکار', 'Workbench navigation')}>{navigation.map(([view, label]) =>
        <button key={view} aria-current={page === view ? 'page' : undefined} onClick={() => setPage(view)}>{label}</button>)}</nav>
      {space && <button className="back" onClick={() => open()}>{t('بازگشت به میزکار', 'Back to workbench')}</button>}
      <div className="identity"><bdi>{user.email}</bdi><button className="link" onClick={async () => {
        if (dirty && !window.confirm(t('پیش‌نویس ذخیره نشده است. خارج می‌شوید؟', 'Sign out with an unsaved draft?'))) return;
        try { await api('/auth/logout', 'POST', {}); setUser(null); setSpace(undefined); setSpaces([]); setDirty(false); setPage('desk'); }
        catch (cause) { setError(errorText(cause, t)); }
      }}>{t('خروج', 'Sign out')}</button></div>
    </aside>
    <main id="content" tabIndex={-1}>
      <header className="topbar standalone">{locale}</header>
      <div className="content">
        <Message text={error} error />
        {page === 'desk' && <>
          <div className="page-heading"><div><h1>{t('میزکار من', 'My workbench')}</h1>
            <p>{t('کسب‌وکارها و تحلیل‌های بازاریابی', 'Your workspaces and marketing analyses')}</p></div>
            <button className="primary" onClick={() => setPage('create')}>{t('کسب‌وکار جدید', 'New workspace')}</button>
          </div>
          <div className="spaces">{spaces.map((company) => <button key={company.id} className="space-card"
            onClick={() => open(company, 'profile')}><span className="space-icon" aria-hidden="true">{company.name.slice(0, 1)}</span>
            <strong>{company.name}</strong><small dir="ltr">{company.currency} · {company.timezone}</small>
          </button>)}</div>
          {!spaces.length && <div className="panel empty">{t('هنوز کسب‌وکاری اضافه نکرده‌اید.', 'You have not added a workspace yet.')}</div>}
        </>}
        {page === 'create' && <WorkspaceForm t={t} onCancel={() => open()} onSave={(company) => {
          setSpaces((previous) => [...previous, company]); open(company, 'profile');
        }} />}
        {page === 'catalog' && <AnalysisPage methods={methods} t={t} onDirty={setDirty} />}
        {space && <div key={space.id}>
          <h1 className="context-title">{space.name}</h1>
          {page === 'profile' && <Profiles base={base} editable={editable} t={t} />}
          {page === 'evidence' && <EvidenceRecords base={base} editable={editable} t={t} />}
          {page === 'datasets' && <Datasets workspace={space} base={base} editable={editable} t={t} />}
          {page === 'history' && <History base={base} t={t} />}
          {page === 'members' && space.role === 'owner' && <Members base={base} t={t} />}
          <div hidden={page !== 'analysis'}>
            <AnalysisPage workspace={space} methods={methods} t={t} onDirty={setDirty} visible={page === 'analysis'} />
          </div>
        </div>}
      </div>
    </main>
  </div>;
}

createRoot(document.getElementById('root')!).render(<App />);
