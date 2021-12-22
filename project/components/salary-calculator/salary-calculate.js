import { useState } from 'react';

import SalaryCalculateForm from './salary-calculate-form';
import Results from './results';

import classes from './salary-calculate-form';

function SalaryCalculate() {
  const [errorState, setError] = useState(null);
  const [displayForm, setDisplayForm] = useState(true);
  const [taxData, setTaxData] = useState(null);
  const [formPayload, setFormPayload] = useState(null);

  async function calculateSalaryHandler(payload) {
    setFormPayload(payload);
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
      setError(null);
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
      {!errorState && taxData && (
        <Results payload={formPayload} taxData={taxData} />
      )}
    </section>
  );
}

export default SalaryCalculate;
