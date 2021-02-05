/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 * @date: 2021-01-31
 */

import * as express from 'express';
import * as morgan from 'morgan';
import * as bodyParser from 'body-parser';

import { Express } from 'express-serve-static-core';

import router from '@/routes';
import headers from '@/middlewares/header.middleware';

const app: Express = express()

// logger
app.use(morgan('common'));
// body parser
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
// set content-type to text/json
app.use(headers);

app.use(router);

app.listen(3000, () => {
  console.log('Starting at 3000')
});