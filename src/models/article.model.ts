import { db } from '../db';
import { TagInterface } from './tag.model';
import { Schema, Document } from 'mongoose';

export interface ArticleInterface extends Document {
    create_at: Date,
    update_at: Date,
    title: string,
    cover: string,
    author: string,
    content: string,
    publish: number, // 0: drafts; 1: private, 2: public
    tags: TagInterface[],
    category: string,
    desc: string
}

const articleSchema: Schema = new db.Schema({
    create_at: { type: Date, default: Date.now },
    update_at: { type: Date, default: Date.now },
    title: { type: String, required: true },
    cover: { type: String, required: true },
    author: { type: String, required: false },
    content: { type: String, required: true },
    publish: { type: Number, default: 1 },
    tags: [{ type: db.Schema.Types.ObjectId, ref: 'Tag' }],
    category: { type: String, required: false },
    desc: { type: String, required: false }
}, {
    versionKey: false,
    timestamps: {
        createdAt: 'create_at',
        updatedAt: 'update_at'
    }
});

const Article = db.model('Article', articleSchema);
export default Article;