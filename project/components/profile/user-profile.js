import { useState } from 'react';

import ProfileForm from './profile-form';

import classes from './user-profile.module.css';

function UserProfile() {
  const [errorState, setError] = useState(false);
  const [successState, setSuccess] = useState(false);

  async function changePasswordHandler(passwordData) {
    const response = await fetch('/api/user/change-password', {
      method: 'PATCH',
      body: JSON.stringify(passwordData),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const responseData = await response.json();

    if (response.status !== 200) {
      setError({
        message: responseData.message,
      });
      setSuccess(false);
    } else {
      setSuccess({
        message: responseData.message
      });
      setError(false);
    }
  }

  return (
    <section className={classes.profile}>
      <h1>Your User Profile</h1>
      <ProfileForm onChangePassword={changePasswordHandler} />
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

export default UserProfile;
