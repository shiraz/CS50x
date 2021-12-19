import { useState } from 'react';

import SalaryCalculateForm from './salary-calculate-form';

import classes from './salary-calculate-form';

function SalaryCalculate() {
  const [errorState, setError] = useState(false);
  const [displayForm, setDisplayForm] = useState(true);
  const [taxData, setTaxData] = useState(null); 

  async function calculateSalaryHandler(payload) {
    const response = await fetch('/api/tax/calculate', {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const responseData = await response.json();

    if (responseData.status !== 200) {
      setError({
        message: responseData.message,
      });
    } else {
      setDisplayForm(false);
      setError(false);
      setTaxData(responseData);
    }
  }

  return (
    <section className={classes.salaryCalculateForm}>
      {displayForm && (
        <SalaryCalculateForm onCalculate={calculateSalaryHandler} />
      )}
      {errorState && (
        <div className='alert alert-danger' role='alert'>
          {errorState.message}
        </div>
      )}
      {taxData && (<p>TO DO</p>)}
    </section>
  );
}

export default SalaryCalculate;
