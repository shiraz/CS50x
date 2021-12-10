import Link from 'next/link';
import { signOut, useSession } from 'next-auth/client';
import { useRouter } from 'next/router';

import classes from './main-navigation.module.css';

function MainNavigation() {
  const [session, loading] = useSession();
  const router = useRouter();

  function logoutHandler() {
    signOut();
  }

  return (
    <header className={classes.header}>
      <Link href='/'>
        <a>
          <div className={classes.logo}>Budgetor</div>
        </a>
      </Link>
      <nav>
        <ul>
          {!session && !loading && (
            <li>
              <a className={router.pathname == '/auth' ? classes.active : ''}>Login</a>
            </li>
          )}
          {session && (
            <li>
              <Link href='/salary-calculator'>
                <a className={router.pathname == '/salary-calculator' ? classes.active : ''}>Salary Calculator</a>
              </Link>
            </li>
          )}
          {session && (
            <li>
              <Link href='/profile'>
                <a className={router.pathname == '/profile' ? classes.active : ''}>Profile</a>
              </Link>
            </li>
          )}
          {session && (
            <li>
              <button onClick={logoutHandler}>Logout</button>
            </li>
          )}
        </ul>
      </nav>
    </header>
  );
}

export default MainNavigation;
