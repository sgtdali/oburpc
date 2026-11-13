import fs from 'node:fs';
import dotenv from 'dotenv';
import {createClient} from '@supabase/supabase-js';
dotenv.config({path:'.env.local',quiet:true});
if(new URL(process.env.NEXT_PUBLIC_SUPABASE_URL).hostname !== 'wvnkyeafczmzgssdgzlq.supabase.co') throw Error('Wrong project');
const db=createClient(process.env.NEXT_PUBLIC_SUPABASE_URL,process.env.SUPABASE_SERVICE_ROLE_KEY,{db:{schema:'skincare'},auth:{persistSession:false}});
const dir='../db-backups/2026-10-05_pre-bioderma-expansion';
fs.mkdirSync(dir,{recursive:true});
for(const table of ['brands','ingredients','products','product_ingredients']){
 const rows=[];
 for(let offset=0;;offset+=500){
  const {data,error}=await db.from(table).select('*').order(table==='product_ingredients'?'product_id':'id').range(offset,offset+499);
  if(error)throw Error(error.message);
  rows.push(...data);if(data.length<500)break;
 }
 const dest=`${dir}/${table}.json`;
 if(fs.existsSync(dest))throw Error('Backup already exists');
 fs.writeFileSync(dest,JSON.stringify(rows,null,2));console.log(table,rows.length);
}
for(const file of ['catalog.json','texts_tr.json'])fs.copyFileSync(`scripts/skincare/${file}`,`${dir}/${file}`,fs.constants.COPYFILE_EXCL);
