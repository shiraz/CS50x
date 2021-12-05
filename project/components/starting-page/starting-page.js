import Hero from './hero';

import classes from './starting-page.module.css';

function StartingPageContent() {
  // Show Link to Login page if NOT auth

  return (
    <section className={classes.starting}>
      <h1>Welcome to Budgetor</h1>
      <Hero />
      <p className='mt-5 text-center text-wrap fs-5'>
        The Budgetor is used to solve a problem that every potential USA
        immigrant faces; how much money does a person actually make after all
        income taxes have been paid?
      </p>
    </section>
  );
}

export default StartingPageContent;
