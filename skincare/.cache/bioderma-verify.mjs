import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import dotenv from 'dotenv';
import {createClient} from '@supabase/supabase-js';
dotenv.config({path:'.env.local',quiet:true});
const url=process.env.NEXT_PUBLIC_SUPABASE_URL;
assert.equal(new URL(url).hostname,'wvnkyeafczmzgssdgzlq.supabase.co');
const service=createClient(url,process.env.SUPABASE_SERVICE_ROLE_KEY,{db:{schema:'skincare'},auth:{persistSession:false}});
const anon=createClient(url,process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,{db:{schema:'skincare'},auth:{persistSession:false}});
const base='scripts/skincare';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const expected=read(`${base}/.cache/bioderma-expected-products.json`);
async function rows(client,table){
 const out=[];
 for(let offset=0;;offset+=500){
  let query=client.from(table).select('*').order(table==='product_ingredients'?'product_id':'id');
  if(table==='product_ingredients')query=query.order('position');
  const {data,error}=await query.range(offset,offset+499);if(error)throw Error(error.message);
  out.push(...data);if(data.length<500)break;
 }return out;
}
const current={};
for(const table of ['brands','ingredients','products','product_ingredients']){
 current[table]=await rows(service,table);
 const old=read(`../db-backups/2026-10-05_pre-bioderma-expansion/${table}.json`);
 const key=r=>table==='product_ingredients'?`${r.product_id}/${r.position}`:r.id;
 const by=new Map(current[table].map(r=>[key(r),r]));
 for(const r of old)assert.deepEqual(by.get(key(r)),r,`Changed old ${table} ${key(r)}`);
 console.log('preserved',table,old.length,'current',current[table].length);
}
const publicProducts=await rows(anon,'products');
const publicIngredients=await rows(anon,'ingredients');
const publicLinks=await rows(anon,'product_ingredients');
const publicMap=new Map(publicProducts.map(p=>[p.slug,p]));
const ingredientSlug=new Map(publicIngredients.map(i=>[i.id,i.slug]));
const brand=current.brands.find(b=>b.slug==='bioderma');
const publicBioderma=publicProducts.filter(p=>p.brand_id===brand.id);
assert.equal(publicBioderma.length,66);
const publicAllowed=new Set(read(`${base}/catalog.json`).products.filter(p=>p.brand==='bioderma').map(p=>p.slug));
assert.deepEqual(new Set(publicBioderma.map(p=>p.slug)),publicAllowed);
let links=0;
for(const p of expected){
 const saved=publicMap.get(p.slug);assert(saved?.published,p.slug);
 const fields={name:'name',nameTr:'name_tr',categorySlug:'category_slug',description:'description',attributes:'attributes',keyIngredientGroups:'key_ingredient_groups',benefits:'benefits',concerns:'concerns',brandClaims:'brand_claims',howTo:'how_to',formulaRegion:'formula_region',sources:'sources'};
 for(const [from,to] of Object.entries(fields))assert.deepEqual(saved[to],p[from],`${p.slug}.${to}`);
 const list=publicLinks.filter(l=>l.product_id===saved.id).sort((a,b)=>a.position-b.position);
 assert.deepEqual(list.map(l=>l.position),p.ingredientSlugs.map((_,i)=>i+1));
 assert.deepEqual(list.map(l=>ingredientSlug.get(l.ingredient_id)),p.ingredientSlugs,p.slug);links+=list.length;
}
let images=0;
for(let start=0;start<expected.length;start+=4){
 await Promise.all(expected.slice(start,start+4).map(async p=>{
  const response=await fetch(publicMap.get(p.slug).image_url);assert(response.ok,p.slug);assert(response.headers.get('content-type').startsWith('image/webp'));
  const actual=Buffer.from(await response.arrayBuffer());const local=fs.readFileSync(`${base}/out/images/${p.imageFile}`);
  assert.equal(crypto.createHash('sha256').update(actual).digest('hex'),crypto.createHash('sha256').update(local).digest('hex'),p.slug);images++;
 }));
 console.log('images verified',images);
}
const result={date:'2026-10-05',project:'wvnkyeafczmzgssdgzlq',addedProducts:expected.length,biodermaTotal:66,addedIngredientLinks:links,publicImagesVerified:images,existingRowsPreserved:true,totals:Object.fromEntries(Object.entries(current).map(([k,v])=>[k,v.length])),products:expected.map(p=>({slug:p.slug,name:p.name,category:p.categorySlug,ingredients:p.ingredientSlugs.length}))};
fs.writeFileSync(`${base}/.cache/bioderma-import-verification.json`,JSON.stringify(result,null,2));
console.log('PASS',JSON.stringify({...result,products:undefined}));
