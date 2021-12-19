import React from 'react';
import Image from 'next/image';

import classes from './hero.module.css';

function Hero() {
    return (
        <section className={classes.hero}>
            <div className={classes.image}>
                <Image src="/images/site/Budgetor_Logo.jpg" alt="Budgetor Logo Alt" width={300} height={300} />
            </div>
        </section>
    )
}

export default Hero;