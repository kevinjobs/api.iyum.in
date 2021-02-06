/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 * @date: 2021-01-31
 */

import mongoose from 'mongoose';
import { MONGDB } from '../config';

(mongoose as any).Promise = global.Promise;

export const db = mongoose;

export const connect = () => {
    mongoose.connect(MONGDB.uri, {
        useNewUrlParser: true,
        useFindAndModify: false,
        useUnifiedTopology: true
    });

    mongoose.connection.on('error', err => {
        console.log(err);
    });

    mongoose.connection.once('open', () => {
        console.log('Connect to db successfully!');
    });

    return mongoose;
}