# BUDGETOR
The Budgetor is used to solve a problem that every potential USA immigrant faces; how much money does a person actually make after all income taxes have been taken out? The site supports net paycheck calculation after federal, FICA and state taxes have been taken out from the gross pay amount.

## GETTING STARTED
First, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in the web browser to see the result.

## VIDEO DEMO
[https://youtu.be/6Qrp9YC_Na0](https://youtu.be/6Qrp9YC_Na0)

## PROJECT DESCRIPTION
This is a Next.js (a React.js framework) site where the project code is split into 5 directories:
1. `pages` - This directory contains files that have React components associated with routes based on the filename as well as REST APIs that calculate taxes, performs user authentication, and password updates.
    1. `api`
        1. `auth/[...nextauth].js` - This API is used to authenticate the user. MongoDB is used as the backend specifically the `users` collection that contains the email address and the hashed password. 
        2. `auth/signup.js` - This API is used to register the user. MongoDB is used as the backend specifically the `users` collection that stores the email address and the hashed password.
        3. `tax/calculate.js` - This API is used to calculate the income taxes based on the user's `Pay Rate`, `Pay Period`, `State`, `Exemptions`, and `Filing Status`. A JSON response is returned containing the income taxes for `Federal`, `State`, and `FICA` for the `Pay Period` as well as annually.
        4. `user/change-password.js` - This API is used to change the user's password.
    2. `pages`
        1. `_app.js` - This is the core component that is used in all page component. This uses the `layout.js` component which wraps all the other page components of this site.
        2. `auth.js` - This page appears after the user clicks on the `Login` link. This page is used to login.
        3. `index.js` - This is the main page of the site. This contains the `hero.js` component.
        4. `profile.js` - This page appears after the user clicks on the `Profile` link. This page appears only after the user is logged in. Attempting to access this page without logging in will result in the user being redirected to the login page.
        5. `salary-calculator.js` - This page appears after the upon successful login. This page contains a form whether the user inputs the salary data to calculate the net pay (total salary after the income taxes are deducted).
2. `components`- This directory contains React components that are to be used in `pages` or other React components.
    1. `auth`
        1. `auth-form.js` - This is the authentication form component. This is used for user authentication, user registration, and user login.
        2. `auth-form.module.css` - This file contains the CSS styles used in the `auth-form.js` component.
    2. `home`
        1. `hero.js` - This is the hero component. This is rendered on the `home.js` component.
        2. `hero.module.css` - This file contains the CSS styles used in the `hero.js` component.
        3. `home.js` - This is the home component. This contains the `hero.js` component as well as other texts that describe what this site is for.
        4. `home.module.css` - This file contains the CSS styles used in the `home.js` component.
    3. `layout`
        1. `layout.js` - This is the layout component. This is used to wrap the main `_app.js` page component so that the global navigation appears in all pages of the site.
        2. `main-navigation.js` - This is the main navigation component. This contains the global navigation links and is rendered in `layout.js` component. This page changes based on the user authentication status. If the user is logged in, then the `Salary Calculator`, `Profile`, and `Logout` links appear in the navigation.
        3. `main-navigation.module.css` - This file contains the CSS styles used in the `main-navigation.js` component.
    4. `profile`
        1. `profile-form.js` - This is the profile form component. This form is used to change the user password.
        2. `profile-form.module.css` - This file contains the CSS styles used in the `profile-form.js` component.
        3. `user-profile.js` - This is the user profile component. This component sends a `PATCH` request to the `change-password` API to change the password, and then renders the result (whether the password was changed successfully or not).
        4. `user-profile.module.css` - This file contains the CSS styles used in the `user-profile.js` component.
    5. `salary-calculator`
        1. `pay-periods.json` - This file contains all the `Pay Period` / `Pay Frequency` dropdown values to be used in the `salary-calculate-form.js` component.
        2. `states.json` - This file contains all the `State` dropdown values to be used in the `salary-calculate-form.js` component.
        3. `statuses.json` - This file contains all the `Filing Status` dropdown values to be used in the `salary-calculate-form.js` component.
        4. `salary-calculate-form.js` - This is the Salary Calculate form component. This form is where the user inputs the salary details to calculate the net salary once the taxes are taken out. 
        5. `salary-calculate-form.module.css` - This file contains the CSS styles used in the `salary-calculate-form.js` component.
        6. `results.js` - This is the results component. This component sends a `POST` request to the `calculate` API, which gives the user all the tax data pertaining to federal, FICA and state. It then formats the response and renders it in two tables showing the net salary based on the `Pay Period` selected and annually.
3. `lib` - This directory contains helper method code for authentication, database and tax operations.
    1. `auth.js` - This JS file contains helper methods for authentication; specifically hashing and verifying passwords.
    2. `db.js` - This JS file contains a method that creates a MongoDB connection to the Atlas cluster.
    3. `tax.js` - This JS file contains helper methods that are to be used in Calculate Tax API (please refer to the `pages` bullet point).
4. `public` - This directory contains the project logo that was used in the site.
5. `styles` - This directory contains global styles that are to be used everywhere in the site.
6. `packages.json` - This file contains all the dependencies that are used in this Next.js site.
7. `packages-lock.json` - This file describes the exact tree that was generated for all operations done during packages/dependencies installation.
8. `node_modules` - This directory contains all the project dependecy files.
9. `.env.local` - This file contains all the secret keys that are to be used in the project; MongoDB Atlas Credentials and the Taxee API key.

### DEPENDENCIES
1. MongoDB Atlas Credentials
2. Taxee API Key
