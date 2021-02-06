import { db } from '../db';
import { Document, Model, Schema } from 'mongoose';

export interface TagInterface extends Document {
    _id: string,
    name: string,
    desc: string,
    amount: number // amount of articles
}

const tagSchema: Schema = new db.Schema({
    name: { type: String, required: true, validate: /\S+/ },
    desc: { type: String, required: true, validate: /\S+/ },
    amount: { type: Number, default: 0 }
}, {
    versionKey: false
});

const Tag: Model<TagInterface> = db.model<TagInterface>("Tag", tagSchema);
export default Tag;