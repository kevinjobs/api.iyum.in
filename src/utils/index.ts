const Hashids = require('hashids/cjs');
// hash id with salt.
export const hashids = new Hashids('mintforge', 8);