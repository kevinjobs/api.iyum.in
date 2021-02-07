/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 */

// import * as fs from 'fs';
import * as sqlite3 from 'sqlite3';

const dbpath = 'myblogdata.db';

// const exists = fs.existsSync(dbpath);

const sqlite = sqlite3.verbose();

const db = new sqlite.Database(dbpath);

export default db;