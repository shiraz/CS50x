import { useRef } from 'react';

import payPeriods from './pay-periods.json';
import states from './states.json';
import statuses from './statuses.json';

import classes from './salary-calculate-form.module.css';

function SalaryCalculateForm(props) {
  const exemptionsRef = useRef();
  const filingStatusRef = useRef();
  const payPeriodRef = useRef();
  const payRateRef = useRef();
  const stateRef = useRef();

  function submitHandler(event) {
    event.preventDefault();
    props.onCalculate({
      state: stateRef.current.value,
      payRate: payRateRef.current.value,
      payPeriod: payPeriodRef.current.value,
      filingStatus: filingStatusRef.current.value,
      exemptions: exemptionsRef.current.value,
    });
  }

  return (
    <section className={classes.salaryCalculateForm}>
      <h1>SALARY CALCULATOR</h1>
      <form onSubmit={submitHandler}>
        <div className={classes.control}>
          <label htmlFor='state'>State</label>
          <select
            className={classes.dropdown}
            defaultValue=''
            ref={stateRef}
            required
          >
            {states.map((currentState) => (
              <option
                key={currentState.short}
                value={currentState.short}
                disabled={currentState.disabled ? true : false}
              >
                {currentState.name}
              </option>
            ))}
          </select>
        </div>

        <div className={classes.control}>
          <label htmlFor='pay-rate'>Pay Rate</label>
          <input
            type='number'
            min='0.01'
            step='0.01'
            required
            ref={payRateRef}
          />
        </div>

        <div className={classes.control}>
          <label htmlFor='pay-period'>Pay Period</label>
          <select
            className={classes.dropdown}
            ref={payPeriodRef}
            defaultValue=''
            required
          >
            {payPeriods.map((payPeriod) => (
              <option
                key={payPeriod.key}
                value={payPeriod.key}
                disabled={payPeriod.disabled ? true : false}
              >
                {payPeriod.period}
              </option>
            ))}
          </select>
        </div>

        <div className={classes.control}>
          <label htmlFor='filing-status'>Filing Status</label>
          <select
            className={classes.dropdown}
            ref={filingStatusRef}
            defaultValue=''
            required
          >
            {statuses.map((status) => (
              <option
                key={status.statusValue}
                value={status.statusValue}
                disabled={status.disabled ? true : false}
              >
                {status.status}
              </option>
            ))}
          </select>
        </div>

        <div className={classes.control}>
          <label htmlFor='exemptions'>Exemptions</label>
          <input type='number' min='0' max='100' required ref={exemptionsRef} />
        </div>

        <div className={classes.actions}>
          <button>CALCULATE</button>
        </div>
      </form>
    </section>
  );
}

export default SalaryCalculateForm;
