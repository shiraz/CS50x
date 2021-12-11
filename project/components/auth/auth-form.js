import { useRef, useState } from 'react';
import { signIn } from 'next-auth/client';
import { useRouter } from 'next/router';

import classes from './auth-form.module.css';

async function createUser(email, password) {
  const response = await fetch('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const responseData = await response.json();

  if (!response.ok) {
    throw new Error(
      responseData.message ||
        'Invalid response detected from /api/auth/signup request'
    );
  }

  return responseData;
}

function AuthForm() {
  const emailInputRef = useRef();
  const passwordInputRef = useRef();

  const [isLogin, setIsLogin] = useState(true);
  const [errorState, setError] = useState(false);
  const [successState, setSuccess] = useState(false);
  const router = useRouter();

  function switchAuthModeHandler() {
    setIsLogin((prevState) => !prevState);
  }

  async function submitHandler(event) {
    event.preventDefault();
    const enteredEmail = emailInputRef.current.value;
    const enteredPassword = passwordInputRef.current.value;

    if (isLogin) {
      const result = await signIn('credentials', {
        redirect: false,
        email: enteredEmail,
        password: enteredPassword,
      });

      if (!result.error) {
        router.replace('/salary-calculator');
      } else {
        setError({
          message: result.error
        });
        setSuccess(false);
      }
      
    } else {
      try {
        const responseData = await createUser(enteredEmail, enteredPassword);
        setError(false);
        setSuccess({
          message: responseData.message
        });
      } catch (error) {
        setError({
          message: error.message
        });
      }
    }
  }

  return (
    <section className={classes.auth}>
      <h1>{isLogin ? 'Sign In' : 'Sign Up'}</h1>
      <form onSubmit={submitHandler}>
        <div className={classes.control}>
          <label htmlFor='email'>Enter Your Email Address</label>
          <input type='email' id='email' required ref={emailInputRef} />
        </div>
        <div className={classes.control}>
          <label htmlFor='password'>Enter Your Password</label>
          <input
            type='password'
            id='password'
            required
            ref={passwordInputRef}
          />
        </div>
        <div className={classes.actions}>
          <button>{isLogin ? 'Login' : 'Create Account'}</button>
          <button
            type='button'
            className={classes.toggle}
            onClick={switchAuthModeHandler}
          >
            {isLogin ? 'Create new account' : 'Login with an existing account'}
          </button>
        </div>
      </form>
      {errorState && (
        <div className='alert alert-danger' role='alert'>
          {errorState.message}
        </div>
      )}
      {successState && (
        <div className='alert alert-success' role='alert'>
          {successState.message}
        </div>
      )}
    </section>
  );
}

export default AuthForm;
