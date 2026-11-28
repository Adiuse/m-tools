import { useState } from 'react';
import { api } from './api';
import type { Translate, User } from './api';
import { Field, formValues, Message, useTask } from './shared';

export type AccountLink = { mode: 'activate' | 'reset'; uid: string; token: string };

export function SessionForm({ t, link, onLogin }: {
  t: Translate; link: AccountLink | null; onLogin: (user: User) => void;
}) {
  const [mode, setMode] = useState<'login' | 'register' | 'reset' | 'password'>(link ? 'password' : 'login');
  const [message, setMessage] = useState('');
  const task = useTask(t);
  const title = {
    login: t('ورود به میزکار', 'Sign in to your workbench'),
    register: t('ساخت حساب', 'Create an account'),
    reset: t('بازیابی رمز', 'Reset your password'),
    password: t('تنظیم رمز عبور', 'Choose a password'),
  }[mode];

  return <main className="session">
    <div className="session-picture">
      <div className="wordmark">M<span>·</span>TOOLS</div>
      <h1>{t('میزکار بازاریابی', 'Marketing workbench')}</h1>
      <p>{t('کسب‌وکارها، شواهد و تحلیل‌های خود را در یک میزکار مدیریت کنید.',
        'Manage your workspaces, evidence, and analyses in one place.')}</p>
    </div>
    <form className="panel session-form" onSubmit={(event) => {
      const data = formValues(event);
      task.run(async () => {
        if (mode === 'login') {
          onLogin((await api<{ user: User }>('/auth/login', 'POST', data)).user);
        } else if (mode === 'password' && link) {
          await api('/auth/password', 'POST', { ...link, ...data });
          setMode('login');
          setMessage(t('رمز ذخیره شد. وارد حساب شوید.', 'Password saved. Sign in to continue.'));
        } else {
          await api('/auth/' + mode, 'POST', data);
          setMessage(t('اگر درخواست معتبر باشد، پیوندی به ایمیلتان می‌رسد.',
            'If the request is valid, a link will be sent to your email.'));
        }
      });
    }}>
      <h2>{title}</h2>
      {mode !== 'password' && <Field label={t('ایمیل', 'Email')}><input name="email" type="email" autoComplete="email" dir="ltr" required /></Field>}
      {(mode === 'login' || mode === 'password') && <Field label={t('رمز عبور', 'Password')}>
        <input name="password" type="password" autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
          minLength={mode === 'password' ? 8 : undefined} required dir="ltr" />
      </Field>}
      <Message text={task.error} error /><Message text={message} />
      <button className="primary" disabled={task.busy}>{mode === 'login' ? t('ورود', 'Sign in') : t('ادامه', 'Continue')}</button>
      <div className="row">
        {(mode === 'login' ? ['register', 'reset'] as const : ['login'] as const).map((next) =>
          <button className="link" key={next} type="button" onClick={() => { setMode(next); setMessage(''); }}>
            {next === 'login' ? t('بازگشت به ورود', 'Back to sign in')
              : next === 'register' ? t('ساخت حساب', 'Create an account') : t('فراموشی رمز', 'Forgot password')}
          </button>)}
      </div>
    </form>
  </main>;
}
