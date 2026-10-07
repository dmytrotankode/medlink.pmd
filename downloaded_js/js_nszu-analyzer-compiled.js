'use strict';
var App = App || {};
const ICON_URLS = {
'note': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><g fill="none" stroke-miterlimit="10" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode:normal"><path d="M128 34.72c48.573 0 88.548 37.329 92.848 84.8h33.92C250.375 53.334 195.28.8 128 .8S5.625 53.334 1.232 119.52h33.92c4.3-47.471 44.275-84.8 92.848-84.8m0 186.56c-48.573 0-88.548-37.329-92.848-84.8H1.232C5.625 202.666 60.72 255.2 128 255.2s122.375-52.534 126.768-118.72h-33.92c-4.3 47.471-44.275 84.8-92.848 84.8" fill="#ed0049"/><path d="M115.28 98.32h25.44v93.28h-25.44zm0-33.92h25.44v25.44h-25.44z" fill="#0f518c"/></g></svg>',
'referral_yes': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><defs><linearGradient x1="12" y1="2" x2="12" y2="22" gradientUnits="userSpaceOnUse" id="rya"><stop offset="0" stop-color="#0086ff"/><stop offset="1" stop-color="#0086ff"/></linearGradient><linearGradient x1="12.5" y1="2.659" x2="12.5" y2="22.335" gradientUnits="userSpaceOnUse" id="ryb"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#a6eafb"/></linearGradient></defs><g fill="none" stroke-miterlimit="10" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode:normal"><path d="M20 8.24V20c0 1.1-.9 2-2 2H6c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h7.76c.79 0 1.56.32 2.12.88l3.24 3.24c.56.56.88 1.33.88 2.12" fill="url(#rya)" transform="translate(-25.6 -25.6)scale(12.8)"/><path d="M15 17c0 .55-.45 1-1 1H8c-.55 0-1-.45-1-1s.45-1 1-1h6c.55 0 1 .45 1 1m1-5H8c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1m1.78-4.3L14.3 4.22c-.48-.47-1.3-.14-1.3.54v3.48c0 .42.34.76.76.76h3.48c.68 0 1.01-.82.54-1.3" fill="url(#ryb)" transform="translate(-25.6 -25.6)scale(12.8)"/></g></svg>',
'referral_no': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><defs><linearGradient x1="12" y1="2" x2="12" y2="22" gradientUnits="userSpaceOnUse" id="rna"><stop offset="0" stop-color="#ff4d4d"/><stop offset="1" stop-color="red"/></linearGradient><linearGradient x1="12.5" y1="2.659" x2="12.5" y2="22.335" gradientUnits="userSpaceOnUse" id="rnb"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#a6eafb"/></linearGradient></defs><g fill="none" stroke-miterlimit="10" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode:normal"><path d="M20 8.24V20c0 1.1-.9 2-2 2H6c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h7.76c.79 0 1.56.32 2.12.88l3.24 3.24c.56.56.88 1.33.88 2.12" fill="url(#rna)" transform="translate(-25.6 -25.6)scale(12.8)"/><path d="M15 17c0 .55-.45 1-1 1H8c-.55 0-1-.45-1-1s.45-1 1-1h6c.55 0 1 .45 1 1m1-5H8c-.55 0-1 .45-1 1s.45 1 1 1h8c.55 0 1-.45 1-1s-.45-1-1-1m1.78-4.3L14.3 4.22c-.48-.47-1.3-.14-1.3.54v3.48c0 .42.34.76.76.76h3.48c.68 0 1.01-.82.54-1.3" fill="url(#rnb)" transform="translate(-25.6 -25.6)scale(12.8)"/></g></svg>',
'prevention': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 97" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path style="opacity:.941" fill="#0e508b" d="M5.5-.5h49v14h-34v68h54v-48h15v62h-84z"/><path style="opacity:.884" fill="#10538b" d="M60.5-.5h3q12.968 13.47 26 27a211 211 0 0 1-29 1z"/><path style="opacity:.954" fill="#00d9ff" d="M40.5 33.5h14v10h11v15h-11v10h-14v-10h-11v-15h11z"/></svg>',
'diagnostic': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 97" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path style="opacity:.941" fill="#0e508b" d="M5.5-.5h49v14h-34v68h54v-48h15v62h-84z"/><path style="opacity:.884" fill="#10538b" d="M60.5-.5h3q12.968 13.47 26 27a211 211 0 0 1-29 1z"/><path style="opacity:.931" fill="#35e500" d="M40.5 33.5h14v10h11v15h-11v10h-14v-10h-11v-15h11z"/></svg>',
'treatment': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 97" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path style="opacity:.941" fill="#0e508b" d="M5.5-.5h49v14h-34v68h54v-48h15v62h-84z"/><path style="opacity:.884" fill="#10538b" d="M60.5-.5h3q12.968 13.47 26 27a211 211 0 0 1-29 1z"/><path style="opacity:.929" fill="#e50000" d="M40.5 33.5h14v10h11v15h-11v10h-14v-10h-11v-15h11z"/></svg>',
'observation_lab': '<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd" viewBox="0 0 2667 2667" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><linearGradient id="ola" gradientUnits="userSpaceOnUse" x1="0" y1="1333.33" x2="2666.66" y2="1333.33"><stop offset="0" style="stop-opacity:1;stop-color:#033b4b"/><stop offset="1" style="stop-opacity:1;stop-color:#108a99"/></linearGradient><linearGradient id="olb" gradientUnits="userSpaceOnUse" xlink:href="#ola" x1="506.354" y1="1333.33" x2="2160.31" y2="1333.33"/></defs><path d="M592 0h1483c325 0 592 266 592 592v1483c0 325-267 592-592 592H592c-326 0-592-267-592-592V592C0 266 266 0 592 0" style="fill:url(#ola)"/><path d="M711 215h1244c273 0 497 223 497 496v1244c0 273-224 497-497 497H711c-273 0-496-224-496-497V711c0-273 223-496 496-496" style="fill:#fff"/><path d="M1973 1251c167 190 205 333 181 429-25 98-113 147-200 147-88 0-176-49-200-147-25-96 14-240 182-431 9-9 23-10 33-2 2 1 3 3 4 4m4-134c-26 0-51-9-70-25l-498-420c-46-39-52-108-13-153 21-25 51-39 83-39 26 0 51 9 70 26l498 419c22 19 36 45 38 74 3 29-6 57-25 79-20 25-51 39-83 39M835 2187c-78 0-153-28-212-77-139-117-156-325-39-464l381-453 737 147-615 730c-63 74-154 117-252 117m150-1017 406-483 3 3 498 419 3 3-174 205zm-48 838c3 0 7-2 10-5 4-6 3-14-2-18l-1-1c-5-4-13-3-18 2-4 6-3 14 2 19 3 2 5 3 9 3m-64-54c4 0 8-1 10-4 5-6 4-14-1-19h-1c-5-5-13-4-18 2-5 5-4 14 2 18 2 2 5 3 8 3m-63-53c4 0 8-1 10-4 5-6 4-14-1-19h-1c-5-5-13-4-18 2-5 5-4 14 2 18 2 2 5 3 8 3m-63-53c4 0 8-2 10-5 5-5 4-13-1-18h-1c-5-5-13-4-18 1-5 6-4 14 2 19 2 2 5 3 8 3m-63-53c4 0 7-2 10-5 5-5 4-14-2-18v-1c-6-4-14-3-18 2-5 6-4 14 2 19 2 2 5 3 8 3m329 122c4 0 7-2 10-4 4-6 4-14-1-19h-1c-6-5-14-4-18 1-5 6-4 14 1 19q4.5 3 9 3m-63-53c4 0 7-2 10-5 4-5 4-13-2-18v-1c-6-4-14-3-18 2-5 6-4 14 1 19q4.5 3 9 3m-63-53c3 0 7-2 10-5 4-5 4-14-2-18v-1c-6-4-14-4-19 2-4 6-3 14 2 19q4.5 3 9 3m-64-54c4 0 8-1 11-4 4-6 3-14-2-19h-1c-5-5-13-4-18 2-4 5-3 14 2 18 3 2 5 3 8 3m-63-53c4 0 8-1 10-4 5-6 4-14-1-19h-1c-5-5-13-4-18 2-5 5-4 14 2 18 2 2 5 3 8 3m329 122c4 0 8-1 10-4 5-6 4-14-1-18l-1-1c-5-5-13-4-18 2-5 5-4 14 2 18 2 2 5 3 8 3m-63-53c4 0 8-1 10-4 5-6 4-14-1-19h-1c-6-5-14-4-18 2-5 5-4 14 2 18 2 2 5 3 8 3m-63-53c4 0 7-2 10-5 5-5 4-13-2-18s-14-4-18 1c-5 6-4 14 2 19 2 2 5 3 8 3m-63-53c4 0 7-2 10-5 4-5 4-14-2-18v-1c-6-4-14-3-18 2-5 6-4 14 1 19q4.5 3 9 3m-63-53c4 0 7-2 10-5 4-6 4-14-2-18v-1c-6-4-14-4-19 2-4 5-3 14 2 19q4.5 3 9 3m329 122c3 0 7-2 9-5 5-5 5-13-1-18v-1c-6-4-14-3-18 2-5 5-4 14 1 19q3 3 9 3m-63-53c3 0 7-2 10-5 4-6 4-14-2-18l-1-1c-5-4-13-4-18 2-4 5-3 14 2 19q3 3 9 3m-64-54c4 0 8-1 10-4 5-6 4-14-1-19h-1c-5-5-13-4-18 2-5 5-3 14 2 18 2 2 5 3 8 3m-63-53c4 0 8-2 10-5 5-5 4-13-1-18h-1c-5-5-13-4-18 1-5 6-4 15 2 19 2 2 5 3 8 3m-63-53c4 0 8-2 10-5 5-5 4-13-1-18l-1-1c-6-4-14-3-18 2-5 6-4 14 2 19 2 2 5 3 8 3m1041 189c10 0 20-1 30-4s19-6 28-11c17-10 30-24 38-42s10-39 9-59c-2-26-11-53-22-77-12-25-26-49-42-71-4-6-12-8-19-3-6 4-7 13-3 19q22.5 31.5 39 66c10 22 18 45 20 68 1 16 0 32-7 46-6 13-15 22-27 29q-9 6-21 9c-7 2-15 3-23 3s-14 6-14 13c0 8 6 14 14 14" style="fill:url(#olb);fill-rule:nonzero"/></svg>',
'observation_gen': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><g fill="none" stroke-miterlimit="10" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode:normal"><path d="M227.386 29.35h-72.939V3.073a3.123 3.123 0 0 0-3.123-3.123H3.072A3.123 3.123 0 0 0-.051 3.072V197.96a28.67 28.67 0 0 0 28.37 28.62h73.246v26.348a3.123 3.123 0 0 0 3.123 3.123h148.24a3.123 3.123 0 0 0 3.123-3.123V58.04a28.733 28.733 0 0 0-28.665-28.69" fill="#231f20"/><path d="M6.195 197.96V6.195h142.006v23.156H81.67a3 3 0 0 0-.625.062q-.937-.062-1.874-.062A28.733 28.733 0 0 0 50.5 58.028l.537 139.957a22.425 22.425 0 0 1-22.237 22.4h-.369A22.425 22.425 0 0 1 6.195 197.96" fill="#ff8e5a"/><path d="M46.285 220.384a28.55 28.55 0 0 0 10.993-22.4l-.537-139.969a22.425 22.425 0 0 1 44.843 0v162.37z" fill="#ffba50"/><path d="M249.805 249.805H107.812V58.04a28.62 28.62 0 0 0-10.825-22.418h130.4a22.443 22.443 0 0 1 22.418 22.418z" fill="#fff"/><path d="M228.754 204.45H128.85a3.123 3.123 0 0 0 0 6.246h99.904a3.123 3.123 0 0 0 0-6.246m0-34.65H128.85a3.123 3.123 0 0 0 0 6.247h99.904a3.123 3.123 0 0 0 0-6.246m0-34.58H128.85a3.123 3.123 0 0 0 0 6.246h99.904a3.123 3.123 0 0 0 0-6.246m0-34.374H128.85a3.123 3.123 0 0 0 0 6.246h99.904a3.123 3.123 0 0 0 0-6.246m0-34.649H128.85a3.123 3.123 0 0 0 0 6.247h99.904a3.123 3.123 0 0 0 0-6.247" fill="#231f20"/></g></svg>',
'age_children': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ff8a00" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a6.5 6.5 0 0 1 13 0"/></svg>',
'age_adults': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#7b2ff7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a6.5 6.5 0 0 1 13 0"/></svg>',
'trauma': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="6 5 36 38" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M24 22C28.4183 22 32 18.4183 32 14C32 9.58172 28.4183 6 24 6C19.5817 6 16 9.58172 16 14C16 18.4183 19.5817 22 24 22ZM24 20C27.3137 20 30 17.3137 30 14C30 10.6863 27.3137 8 24 8C20.6863 8 18 10.6863 18 14C18 17.3137 20.6863 20 24 20Z" fill="currentColor"/><path fill-rule="evenodd" clip-rule="evenodd" d="M41 33C41 28.0294 36.9706 24 32 24H16C11.0294 24 7 28.0294 7 33C7 37.9706 11.0294 42 16 42H24C26.2091 42 28 40.2091 28 38C28 36.0944 26.6675 34.5 24.8834 34.0979L28.1731 26H32C35.866 26 39 29.134 39 33C39 36.866 35.866 40 32 40V36C33.6569 36 35 34.6569 35 33C35 31.3431 33.6569 30 32 30H30V42H32C36.9706 42 41 37.9706 41 33ZM16 26C12.134 26 9 29.134 9 33C9 34.811 9.68775 36.4614 10.8163 37.7043L13.5153 34.6814C13.1904 34.2022 13 33.6235 13 33C13 31.3431 14.3431 30 16 30H17.6951L21.2665 26H16ZM24.1094 36.0029L22.4856 40H24C25.1046 40 26 39.1046 26 38C26 36.9321 25.1631 36.0598 24.1094 36.0029ZM20.3269 40L26.0144 26H23.9477L12.3588 38.9796C13.4197 39.627 14.6663 40 16 40H20.3269ZM33 33C33 33.5523 32.5523 34 32 34V32C32.5523 32 33 32.4477 33 33ZM15.9055 32.0044C15.3975 32.052 15 32.4796 15 33L15.0002 33.0183L15.9055 32.0044Z" fill="currentColor"/></svg>'
};
const NOTES_CONFIG = {
episodeTypes: ['prevention', 'diagnostic', 'treatment'],
fieldMapping: {
dsg: {
noteFields: ['additional_requirements', 'additional_requirements_code'],
codeField: 'additional_requirements_code_btn',
referralField: 'additional_requirements_referral',
episodeField: 'episode',
mainTextField: 'drg'
},
package9: {
noteFields: ['Примітка', 'additional_requirements', 'additional_requirements_code'],
codeField: 'additional_requirements_code_btn',
referralField: 'additional_requirements_referral',
episodeField: 'episode',
mainTextField: 'Клас'
}
}
};
function onDOMReady(callback) {
if (document.readyState === 'loading') {
document.addEventListener('DOMContentLoaded', callback);
} else {
callback();
}
}
class NotesSystem {
constructor() {
this.templates = null;
this.initialized = false;
}
async initialize() {
if (this.initialized) return;
if (this._promise) return this._promise;
this._promise = this._doInit();
return this._promise;
}
async _doInit() {
try {
const response = await fetch('/serve.php?f=json/additional-requirements-templates');
if (response.ok) {
this.templates = await response.json();
} else {
this.templates = {};
}
} catch (e) {
this.templates = {};
}
this.initialized = true;
}
expandText(templateId) {
if (!templateId || !this.templates) return templateId;
if (templateId.includes('.')) {
const [section, key] = templateId.split('.');
if (this.templates[section]?.[key]) {
return this.templates[section][key];
}
return templateId;
}
return this.templates.templates?.[templateId] || 
this.templates.packages?.[templateId] || 
this.templates.referrals?.[templateId] ||
this.templates.episodes?.[templateId] ||
this.templates.interventions?.[templateId] ||
templateId;
}
getIconUrl(iconType) {
const svg = ICON_URLS[iconType];
if (!svg) return '';
const uid = ++NotesSystem._uid;
return svg
.replace(/id="([^"]+)"/g, `id="$1_${uid}"`)
.replace(/url\(#([^)]+)\)/g, `url(#$1_${uid})`)
.replace(/xlink:href="#([^"]+)"/g, `xlink:href="#$1_${uid}"`);
}
extractNotesData(item, packageType = 'dsg') {
if (!item || typeof item !== 'object') {
return {
noteText: null,
additionalCodes: null,
referral: null,
episodes: [],
additionalRequirements: null
};
}
const mapping = NOTES_CONFIG.fieldMapping[packageType] || NOTES_CONFIG.fieldMapping.dsg;
const noteTexts = new Set();
for (const field of mapping.noteFields) {
if (item[field]) {
let fieldText = '';
if (typeof item[field] === 'string') {
fieldText = this.expandText(item[field]);
} else if (Array.isArray(item[field])) {
fieldText = item[field].map(id => this.expandText(String(id))).filter(Boolean).join('\n');
} else if (typeof item[field] === 'object') {
fieldText = item[field]["Примітка"] || JSON.stringify(item[field]);
}
if (fieldText.trim()) {
noteTexts.add(fieldText.trim());
}
}
}
const noteText = Array.from(noteTexts).join('\n\n');
const additionalCodes = item[mapping.codeField] || null;
const referral = item[mapping.referralField] || null;
const episodes = Array.isArray(item[mapping.episodeField]) ? item[mapping.episodeField] : [];
const additionalRequirements = this.collectAdditionalRequirements(item);
return {
noteText: noteText || null,
additionalCodes: Array.isArray(additionalCodes) ? additionalCodes : null,
referral,
episodes,
additionalRequirements
};
}
collectAdditionalRequirements(item) {
const requirements = {};
const relevantKeys = Object.keys(item).filter(key => 
key.startsWith('additional_requirements') && item[key]
);
for (const key of relevantKeys) {
const val = item[key];
requirements[key] = Array.isArray(val)
? val.map(id => this.expandText(String(id))).filter(Boolean).join('\n')
: this.expandText(val);
}
return relevantKeys.length > 0 ? requirements : null;
}
createNoteIconHtml(noteText, additionalCodes = null, serviceCode = '', additionalRequirements = null, useUniqueId = false) {
if (!noteText && !additionalCodes?.length) return '';
let escapedText = (noteText || '').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
if (useUniqueId) {
escapedText += `<!--${Date.now() + Math.random()}-->`;
}
const iconUrl = this.getIconUrl('note');
let html = `<span class="note-icon" data-info="${escapedText}"`;
if (additionalCodes && additionalCodes.length > 0) {
const escapedCodes = JSON.stringify(additionalCodes).replace(/"/g, '&quot;').replace(/'/g, '&#39;');
const escapedServiceCode = serviceCode.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
html += ` data-additional-codes="${escapedCodes}" data-service-code="${escapedServiceCode}"`;
}
if (additionalRequirements) {
const escapedRequirements = JSON.stringify(additionalRequirements).replace(/"/g, '&quot;').replace(/'/g, '&#39;');
html += ` data-additional-requirements="${escapedRequirements}"`;
}
html += `>${iconUrl}</span>`;
return html;
}
createEpisodeIconsHtml(episodes, useUniqueId = false) {
if (!Array.isArray(episodes) || episodes.length === 0) return '';
let html = '';
NOTES_CONFIG.episodeTypes.forEach(episodeType => {
if (episodes.some(ep => (ep || '').trim().toLowerCase() === episodeType)) {
let epText = this.expandText(`episodes.${episodeType}`);
if (useUniqueId) {
epText += `<!--${Date.now() + Math.random()}-->`;
}
const escapedEpText = epText.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
const episodeIconUrl = this.getIconUrl(episodeType);
html += `<span class="episode-icon" data-info="${escapedEpText}">${episodeIconUrl}</span>`;
}
});
return html;
}
createReferralIconHtml(referral, useUniqueId = false) {
if (!referral) return '';
const referralType = referral.toLowerCase() === 'yes' ? 'yes' : 'no';
let referralText = this.expandText(`referrals.${referralType}`);
if (useUniqueId) {
referralText += `<!--${Date.now() + Math.random()}-->`;
}
const escapedReferral = referralText.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
const referralIconUrl = this.getIconUrl('referral_' + referralType);
return `<span class="referral-icon" data-info="${escapedReferral}">${referralIconUrl}</span>`;
}
createAgeScopeIconsHtml(scope, useUniqueId = false) {
if (!scope) return '';
const mk = (iconType, text) => {
let t = text;
if (useUniqueId) t += `<!--${Date.now() + Math.random()}-->`;
const escaped = t.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
return `<span class="age-scope-icon" data-info="${escaped}">${this.getIconUrl(iconType)}</span>`;
};
const icons = [];
if (scope.children === 'yes') icons.push(mk('age_children', 'Застосовується для дітей'));
if (scope.adults === 'yes') icons.push(mk('age_adults', 'Застосовується для дорослих<br>(крім пацієнтів з кодами Y36 та Y96)'));
return icons.length > 0 ? `<span class="icons-group">${icons.join('')}</span>` : '';
}
createIconsHtml(notesData, serviceCode = '', useUniqueId = false) {
const icons = [];
if (notesData.noteText || notesData.additionalCodes?.length) {
icons.push(this.createNoteIconHtml(
notesData.noteText, 
notesData.additionalCodes, 
serviceCode, 
notesData.additionalRequirements, 
useUniqueId
));
}
if (notesData.episodes.length > 0) {
icons.push(this.createEpisodeIconsHtml(notesData.episodes, useUniqueId));
}
if (Array.isArray(notesData.observation_lab) && notesData.observation_lab.length) {
const e = JSON.stringify(notesData.observation_lab).replace(/"/g,'&quot;');
const escapedServiceCode = serviceCode.replace(/"/g,'&quot;').replace(/'/g,'&#39;');
icons.push(
`<span class="observation-icon" data-observations="${e}" data-service-code="${escapedServiceCode}" data-info="Переглянути спостереження">
${this.getIconUrl('observation_lab')}
<span class="item-count">${notesData.observation_lab.length}</span>
</span>`
);
}
if (Array.isArray(notesData.observation_gen) && notesData.observation_gen.length) {
const e = JSON.stringify(notesData.observation_gen).replace(/"/g,'&quot;');
const escapedServiceCode = serviceCode.replace(/"/g,'&quot;').replace(/'/g,'&#39;');
icons.push(
`<span class="observation-icon" data-observations="${e}" data-service-code="${escapedServiceCode}" data-info="Переглянути спостереження">
${this.getIconUrl('observation_gen')}
<span class="item-count">${notesData.observation_gen.length}</span>
</span>`
);
}
if (notesData.referral) {
icons.push(this.createReferralIconHtml(notesData.referral, useUniqueId));
}
return icons.length > 0 ? `<span class="icons-group">${icons.join('')}</span>` : '';
}
createElementWithIcons(mainText, item, packageType = 'dsg', useUniqueId = false) {
if (!item) return mainText;
const notesData = this.extractNotesData(item, packageType);
const iconsHtml = this.createIconsHtml(notesData, mainText, useUniqueId);
if (!iconsHtml) {
return mainText.replace(/\s+-\s+/g, '\u00A0-\u00A0');
}
return `
<div style="display: flex; justify-content: space-between; align-items: center;">
<span>${mainText}</span>
${iconsHtml}
</div>
`;
}
}
const notesSystem = new NotesSystem();
NotesSystem._uid = 0;
App.notesSystem = notesSystem;
App.REQUIREMENTS_TEMPLATES = null;
App.expandRequirementText = function(templateId) { return notesSystem.expandText(templateId); };
App.createDSGRowHtml = function(item, packageType = 'dsg') {
const mapping = NOTES_CONFIG.fieldMapping[packageType] || NOTES_CONFIG.fieldMapping.dsg;
const mainText = item[mapping.mainTextField] || '';
return notesSystem.createElementWithIcons(mainText, item, packageType, false);
};
onDOMReady(() => notesSystem.initialize());
function debounce(func, wait) {
let timeout;
return function (...args) {
clearTimeout(timeout);
timeout = setTimeout(() => func.apply(this, args), wait);
};
}
function initTooltipSystem() {
if (initTooltipSystem._done) return;
initTooltipSystem._done = true;
const ac = new AbortController();
const opts = { passive: true, signal: ac.signal };
initTooltipSystem._cleanup = () => ac.abort();
const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
let activeTooltip = null;
let resizeObserver = null;
let activeTarget = null;
let showTimeout = null;
let hideTimeout = null;
function isElementVisible(element) {
const rect = element.getBoundingClientRect();
const containerSelectors = ['#dsg-table-container', '#modal-list', '#tab-content'];
for (const selector of containerSelectors) {
const container = element.closest(selector);
if (container) {
const containerRect = container.getBoundingClientRect();
return (
rect.top >= containerRect.top &&
rect.left >= containerRect.left &&
rect.bottom <= containerRect.bottom &&
rect.right <= containerRect.right &&
rect.width > 0 &&
rect.height > 0
);
}
}
return (
rect.top >= 0 &&
rect.left >= 0 &&
rect.bottom <= window.innerHeight &&
rect.right <= window.innerWidth &&
rect.width > 0 &&
rect.height > 0
);
}
function showTooltip(icon, immediate = false) {
clearTimeout(showTimeout);
clearTimeout(hideTimeout);
if (!isElementVisible(icon)) {
hideTooltip();
return;
}
if (activeTarget === icon && activeTooltip) {
return;
}
hideTooltip();
let content = icon.dataset.info;
if (!content) return;
if (App.expandRequirementText) {
content = App.expandRequirementText(content);
}
const showAction = () => {
try {
activeTarget = icon;
activeTarget.classList.add('tooltip-active');
let parentRow = activeTarget.closest('tr, li, .dsg-row');
if (parentRow) {
parentRow.classList.add('tooltip-row-active');
}
activeTooltip = document.createElement('div');
activeTooltip.className = 'tooltip-popup';
activeTooltip.innerHTML = content.replace(/<!--[^>]*-->/g, '');
const additionalCodes = icon.dataset.additionalCodes;
const serviceCode = icon.dataset.serviceCode;
const additionalRequirements = icon.dataset.additionalRequirements;
if (additionalCodes && serviceCode) {
let codesArray;
try { codesArray = JSON.parse(additionalCodes); } catch(e) { codesArray = []; }
const button = document.createElement('button');
button.className = 'additional-codes-btn';
button.textContent = `Переглянути інтервенції (${codesArray.length})`;
const tooltipText = activeTooltip.innerHTML;
let contextLabel = '';
if (parentRow) {
const titleCell = parentRow.querySelector('.dsg-cell-main, td:first-child');
if (titleCell) {
const textSpan = titleCell.querySelector('span:first-child');
contextLabel = textSpan ? textSpan.textContent.trim() : titleCell.textContent.trim();
}
}
if (!contextLabel) {
contextLabel = serviceCode;
}
const modalTitle = tooltipText + (contextLabel ? ` | ${contextLabel}` : '');
button.onclick = () => {
const activeRow = activeTarget.closest('tr, li, .dsg-row');
if (App.modalManager) {
if (activeRow) App.modalManager.setActiveRow(activeRow);
App.modalManager.showAdditionalCodesModal(serviceCode, codesArray, modalTitle);
}
hideTooltip();
};
activeTooltip.appendChild(button);
}
if (additionalRequirements) {
let requirementsData;
try { requirementsData = JSON.parse(additionalRequirements); } catch(e) { requirementsData = null; }
if (requirementsData) {
const hasPackages = Object.keys(requirementsData).some(key =>
key.startsWith('additional_requirements_package_')
);
if (hasPackages) {
const button = document.createElement('button');
button.className = 'additional-codes-btn';
const row = icon.closest('tr, .dsg-row');
let rowTitle = '';
if (row) {
const mainCell = row.querySelector('.dsg-cell-main, td:first-child');
if (mainCell) {
const textSpan = mainCell.querySelector('span:first-child');
rowTitle = textSpan ? textSpan.textContent.trim() : mainCell.textContent.trim();
}
}
button.textContent = 'Детальніше';
button.onclick = () => {
let bodyContent = '';
Object.keys(requirementsData).forEach(key => {
if (key.startsWith('additional_requirements_package_')) {
bodyContent += `<p>${requirementsData[key]}</p>`;
}
});
const modalTitle = rowTitle ? `Детальніше | ${rowTitle}` : 'Детальніше';
if (row) {
row.classList.add('force-hover');
if (window.miniModal) {
window.miniModal.lastActiveRow = row;
}
}
if (window.miniModal) {
const safeTitle = requirementsData.additional_requirements || '';
window.miniModal.show(modalTitle, `
<div class="appendix-title">${safeTitle}</div>
<div style="font-style: italic;">${bodyContent}</div>`);
}
hideTooltip();
};
activeTooltip.appendChild(button);
}
} 
}
activeTooltip.style.zIndex = (window._modalZTop || 9999) + 1;
document.body.appendChild(activeTooltip);
positionTooltip();
resizeObserver = new ResizeObserver(() => {
if (activeTooltip) positionTooltip();
});
resizeObserver.observe(document.documentElement);
if (!isTouchDevice) {
activeTooltip.addEventListener('mouseleave', (e) => {
const related = e.relatedTarget;
if (!related || (!activeTarget.contains(related) && !activeTooltip.contains(related))) {
hideTimeout = setTimeout(hideTooltip, 100);
}
});
activeTooltip.addEventListener('mouseenter', () => {
activeTarget.classList.add('tooltip-active');
let parentRow2 = activeTarget.closest('tr, li, .dsg-row');
if (parentRow2) {
parentRow2.classList.add('tooltip-row-active');
}
clearTimeout(hideTimeout);
});
}
} catch (err) {
console.error('Tooltip error:', err);
hideTooltip();
}
};
if (immediate) {
showAction();
} else {
showTimeout = setTimeout(showAction, isTouchDevice ? 0 : 100);
}
}
function positionTooltip() {
if (!activeTooltip || !activeTarget) return;
if (!document.contains(activeTarget)) return hideTooltip();
if (!isElementVisible(activeTarget)) {
activeTooltip.style.display = 'none';
return;
}
activeTooltip.style.display = 'block';
activeTooltip.classList.remove('tooltip-bottom', 'tooltip-left', 'tooltip-right');
activeTooltip.offsetHeight;
const rect = activeTarget.getBoundingClientRect();
const tooltipRect = activeTooltip.getBoundingClientRect();
const margin = 15;
const effectiveWidth = window.innerWidth;
const iconX = rect.left + rect.width / 2 + window.pageXOffset;
const iconY = rect.top + rect.height / 2 + window.pageYOffset;
let left = iconX - tooltipRect.width / 2;
let top = rect.bottom + window.pageYOffset + 8;
const screenHeight = window.innerHeight;
const scrollTop = window.pageYOffset;
const scrollLeft = window.pageXOffset;
if (top + tooltipRect.height > screenHeight + scrollTop - margin) {
top = rect.top + scrollTop - tooltipRect.height - 8;
activeTooltip.classList.add('tooltip-bottom');
}
if (top < scrollTop + margin) {
top = iconY - tooltipRect.height / 2;
if (rect.right + tooltipRect.width + 8 < effectiveWidth - margin) {
left = rect.right + scrollLeft + 8;
activeTooltip.classList.add('tooltip-right');
} else {
left = rect.left + scrollLeft - tooltipRect.width - 8;
activeTooltip.classList.add('tooltip-left');
}
}
left = Math.max(margin + scrollLeft, Math.min(left, effectiveWidth + scrollLeft - tooltipRect.width - margin));
top = Math.max(scrollTop + margin, Math.min(top, screenHeight + scrollTop - tooltipRect.height - margin));
if (activeTooltip.classList.contains('tooltip-left') || activeTooltip.classList.contains('tooltip-right')) {
const arrowTop = Math.max(16, Math.min(tooltipRect.height - 16, iconY - top));
activeTooltip.style.setProperty('--arrow-top', arrowTop + 'px');
} else {
const arrowLeft = Math.max(16, Math.min(tooltipRect.width - 16, iconX - left));
activeTooltip.style.setProperty('--arrow-left', arrowLeft + 'px');
}
activeTooltip.style.left = left + 'px';
activeTooltip.style.top = top + 'px';
}
function hideTooltip() {
clearTimeout(showTimeout);
clearTimeout(hideTimeout);
if (activeTarget) {
activeTarget.classList.remove('tooltip-active');
const parentRow = activeTarget.closest('tr, li, .dsg-row');
if (parentRow) {
parentRow.classList.remove('tooltip-row-active');
}
}
if (activeTooltip) {
activeTooltip.remove();
activeTooltip = null;
}
if (activeTarget && isTouchDevice) {
activeTarget.blur();
}
if (resizeObserver) {
resizeObserver.disconnect();
resizeObserver = null;
}
activeTarget = null;
}
document.addEventListener('scroll', function(e) {
if (isTouchDevice || e.target?.closest?.('#modal')) hideTooltip();
else positionTooltip();
}, { capture: true, passive: true, signal: ac.signal });
const selector = '[data-info]';
if (!isTouchDevice) {
document.body.addEventListener('mouseover', (e) => {
const icon = e.target.closest(selector);
if (icon && icon.dataset.info) {
clearTimeout(hideTimeout);
showTooltip(icon);
}
}, opts);
document.body.addEventListener('mouseout', (e) => {
const icon = e.target.closest(selector);
if (icon && !e.relatedTarget?.closest('.tooltip-popup')) {
hideTimeout = setTimeout(() => {
if (activeTarget === icon) hideTooltip();
}, 100);
}
}, opts);
}
document.body.addEventListener('click', (e) => {
const icon = e.target.closest(selector);
if (isTouchDevice) {
const observationIcon = e.target.closest('.observation-icon');
if (observationIcon && observationIcon.dataset.observations) return;
if (icon && icon.dataset.info) {
e.preventDefault();
e.stopPropagation();
if (activeTarget === icon) hideTooltip();
else showTooltip(icon, true);
} else {
hideTooltip();
}
}
}, { signal: ac.signal });
document.addEventListener('click', (e) => {
setTimeout(() => {
if (activeTarget && !document.contains(activeTarget)) hideTooltip();
}, 50);
}, { capture: true, signal: ac.signal });
window.hideActiveTooltip = hideTooltip;
}
function initScrollToTop() {
const btn = document.getElementById("scrollToTop");
if (btn) {
window.addEventListener("scroll", () => {
btn.style.display = window.scrollY > 300 ? "block" : "none";
});
btn.addEventListener("click", () => {
window.scrollTo({ top: 0, behavior: "smooth" });
});
}
}
function showEmptyTableState(message) {
message = message || 'Нічого не знайдено. Спробуйте змінити критерії пошуку.';
const cont = document.getElementById('dsg-table-container');
if (!cont) return;
const tableEl = cont.querySelector('table') || cont.querySelector('.dsg-table-div');
if (tableEl) tableEl.style.display = 'none';
let emptyMessage = document.getElementById('empty-message');
if (!emptyMessage) {
emptyMessage = document.createElement('div');
emptyMessage.id = 'empty-message';
emptyMessage.className = 'empty-message';
cont.parentNode.insertBefore(emptyMessage, cont.nextSibling);
}
emptyMessage.innerHTML =
'<div class="empty-message-inner">' +
'<svg class="empty-message-icon" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">' +
'<circle cx="31" cy="31" r="18" stroke="currentColor" stroke-width="3.5"/>' +
'<line x1="44" y1="44" x2="58" y2="58" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/>' +
'<line x1="23" y1="31" x2="39" y2="31" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>' +
'</svg>' +
'<p class="empty-message-title">' + (message || 'Збігів не знайдено') + '</p>' +
'<p class="empty-message-sub">Спробуйте змінити або скинути фільтри</p>' +
'</div>';
emptyMessage.style.display = 'block';
cont.classList.remove('visible');
}
function hideEmptyTableState() {
const cont = document.getElementById('dsg-table-container');
if (!cont) return;
const tableEl = cont.querySelector('table') || cont.querySelector('.dsg-table-div');
if (tableEl) {
tableEl.style.display = tableEl.tagName === 'TABLE' ? 'table' : '';
}
const emptyMessage = document.getElementById('empty-message');
if (emptyMessage) emptyMessage.style.display = 'none';
cont.classList.add('visible');
}
App.showSearchWarning = function() {
const group = document.querySelector('.meta-info-group');
if (!group) return;
let warning = document.getElementById('search-accuracy-warning');
if (!warning) {
warning = document.createElement('div');
warning.id = 'search-accuracy-warning';
warning.className = 'search-accuracy-warning';
warning.innerHTML =
'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>' +
' Пошук виконується за ключовими фразами. Для точного збігу оберіть значення зі списку.';
group.appendChild(warning);
}
warning.style.display = 'inline-flex';
};
App.hideSearchWarning = function() {
const warning = document.getElementById('search-accuracy-warning');
if (warning) warning.style.display = 'none';
};
App.updateSearchWarning = function() {
const maps = [];
if (typeof CF !== 'undefined') maps.push(...Object.values(CF).filter(m => m instanceof Map));
const hasPartial = maps.some(m => [...m.keys()].some(k => k.startsWith('__partial__:')));
hasPartial ? App.showSearchWarning() : App.hideSearchWarning();
};
document.addEventListener('click', function(e) {
var btn = e.target.closest('.pmg-action-btn');
if (!btn) return;
var group = btn.closest('.pmg-package-actions');
var pkg = (group && group.dataset.package)
|| document.querySelector('.pmg-package-badge-num')?.textContent?.trim();
if (!pkg) return;
var action = btn.dataset.action;
var file = '';
if (action === 'procurement') file = pkg + '_procurement_conditions';
if (action === 'explain') file = pkg + '_clarification';
if (action === 'list') file = pkg + '_list';
if (!file) return;
App.modalManager.showIframe('/serve.php?f=info/' + file);
});
App.debounce = debounce;
App.showEmptyTableState = showEmptyTableState;
App.hideEmptyTableState = hideEmptyTableState;
App.initTooltipSystem = initTooltipSystem;
window.initScrollToTop = initScrollToTop;
if (document.readyState === 'loading') {
document.addEventListener('DOMContentLoaded', initTooltipSystem, { once: true });
} else {
initTooltipSystem();
}
(function () {
'use strict';
const ENDPOINT = '/serve.php?f=analyze-nszu';
window.ExcelAnalyzer = {
async analyzeWithProgress(file, onProgress) {
try {
if (onProgress) onProgress(0, 5, 'Підготовка файлу...');
const formData = new FormData();
formData.append('file', file);
const result = await new Promise((resolve, reject) => {
const xhr = new XMLHttpRequest();
window._nszuXhr = xhr;
xhr.open('POST', ENDPOINT);
xhr.responseType = 'blob';
xhr.timeout = 600000;
const csrfMeta = document.querySelector('meta[name="csrf-token"]');
if (csrfMeta) xhr.setRequestHeader('X-CSRF-Token', csrfMeta.content);
let serverFakeTimer = null;
xhr.upload.addEventListener('progress', (e) => {
if (e.lengthComputable) {
const realPct = Math.round((e.loaded / e.total) * 100);
const mbLoaded = (e.loaded / 1024 / 1024).toFixed(1);
const mbTotal = (e.total / 1024 / 1024).toFixed(1);
const step1El = document.getElementById('progStep1');
if (step1El) {
let pctSpan = document.getElementById('uploadPctSpan');
if (!pctSpan) {
pctSpan = document.createElement('span');
pctSpan.id = 'uploadPctSpan';
pctSpan.className = 'analyzer-step-lbl'; 
step1El.appendChild(pctSpan); 
}
pctSpan.textContent = `(${mbLoaded} з ${mbTotal} МБ - ${realPct}%)`;
}
if (onProgress) onProgress(1, Math.round(realPct * 0.2), 'Відправка файлу...');
}
});
xhr.upload.addEventListener('loadend', () => {
const pctSpan = document.getElementById('uploadPctSpan');
if (pctSpan && file) {
const mbTotal = (file.size / 1024 / 1024).toFixed(1);
pctSpan.textContent = `(${mbTotal} з ${mbTotal} МБ - 100%)`;
}
let serverPct = 20; 
if (onProgress) onProgress(2, serverPct, 'Розпакування файлу...');
const expectedSeconds = Math.max(10, (file.size / 1024 / 1024) * 2.5); 
const incrementPerTick = (98 - 20) / (expectedSeconds * 2);
serverFakeTimer = setInterval(() => {
if (serverPct < 98) {
serverPct += incrementPerTick; 
if (serverPct > 98) serverPct = 98;
}
let currentStep = 2;
let title = 'Розпакування файлу...';
if (serverPct >= 35) {
currentStep = 3;
title = 'Пошук пакетів та розрахунок...';
}
if (onProgress) onProgress(currentStep, Math.round(serverPct), title);
}, 500);
});
xhr.addEventListener('progress', (e) => {
if (serverFakeTimer) clearInterval(serverFakeTimer);
if (onProgress) onProgress(4, 98, 'Формування файлу...');
});
xhr.onload = () => {
if (serverFakeTimer) clearInterval(serverFakeTimer);
clearInterval(window._analyzeTimer);
window._nszuXhr = null;
if (xhr.status === 200) {
if (onProgress) onProgress(4, 100, 'Готово!');
const blob = xhr.response;
const rawName = xhr.getResponseHeader('X-Filename') || '';
const filename = rawName
? decodeURIComponent(rawName)
: file.name.replace(/\.xlsx$/i, '') + '_analyzed.xlsx';
let stats = null;
try { stats = JSON.parse(xhr.getResponseHeader('X-Stats')); } catch (e) {}
resolve({ success: true, filename, blobUrl: URL.createObjectURL(blob), stats });
} else {
const reader = new FileReader();
reader.onload = () => {
let msg = 'Помилка сервера (' + xhr.status + ')';
let hint = '';
try {
const parsed = JSON.parse(reader.result);
msg = parsed.error || msg;
hint = parsed.hint || '';
} catch (e) {}
reject(new Error(hint ? msg + '\n' + hint : msg));
};
reader.readAsText(xhr.response);
}
};
xhr.onerror = () => { if (serverFakeTimer) clearInterval(serverFakeTimer); clearInterval(window._analyzeTimer); window._nszuXhr = null; reject(new Error('Помилка мережі')); };
xhr.ontimeout = () => { if (serverFakeTimer) clearInterval(serverFakeTimer); clearInterval(window._analyzeTimer); window._nszuXhr = null; reject(new Error('Час очікування вичерпано (більше 10 хв)')); };
xhr.onabort = () => { if (serverFakeTimer) clearInterval(serverFakeTimer); clearInterval(window._analyzeTimer); window._nszuXhr = null; reject(new Error('Аналіз скасовано')); };
xhr.send(formData);
});
return result;
} catch (e) {
clearInterval(window._analyzeTimer);
console.error('[ExcelAnalyzer]', e);
return { success: false, error: e.message };
}
},
async analyze(file, statusEl) {
const status = (msg) => { if (statusEl) statusEl.textContent = msg; };
try {
status('Завантаження на сервер...');
const r = await this.analyzeWithProgress(file, null);
status(r.success ? '✅ Готово! Файл «' + r.filename + '» готовий.' : '❌ ' + r.error);
return r;
} catch (e) {
status('❌ ' + e.message);
return { success: false, error: e.message };
}
}
};
window.addEventListener('beforeunload', () => {
if (window._nszuXhr) { window._nszuXhr.abort(); window._nszuXhr = null; }
});
document.addEventListener('DOMContentLoaded', function () {
const mainCard = document.getElementById('analyzerMainCard');
if (!mainCard) return;
const states = {
empty : document.getElementById('stateEmpty'),
ready : document.getElementById('stateReady'),
progress : document.getElementById('stateProgress'),
result : document.getElementById('stateResult'),
error : document.getElementById('stateError'),
};
const footerElements = {
hint: document.querySelector('.analyzer-hint-txt'),
file: document.querySelector('.analyzer-file-col'),
consent: document.querySelector('.analyzer-consent-col'),
runBtn: document.getElementById('readyRunBtn'),
cancelBtn: document.getElementById('cancelBtn'),
resultActions: document.querySelector('.analyzer-result-actions'),
retryBtn: document.getElementById('errRetryBtn')
};
const fileInput = document.getElementById('analyzerFileInput');
const dropZone = document.getElementById('analyzerDropZone');
const readyFileName = document.getElementById('readyFileName');
const readyFileSize = document.getElementById('readyFileSize');
const readyRunBtn = document.getElementById('readyRunBtn');
const consentCb = document.getElementById('analyzerConsent');
const readyRemove = document.getElementById('readyRemove');
const progTitle = document.getElementById('progTitle');
const progPct = document.getElementById('progPct');
const progFill = document.getElementById('progFill');
const cancelBtn = document.getElementById('cancelBtn');
const progSteps = [
document.getElementById('progStep0'),
document.getElementById('progStep1'),
document.getElementById('progStep2'),
document.getElementById('progStep3'),
document.getElementById('progStep4'),
];
const resTotal = document.getElementById('resTotal');
const resMatched = document.getElementById('resMatched');
const resSkipped = document.getElementById('resSkipped');
const resDlBtn = document.getElementById('resDlBtn');
const resNewBtn = document.getElementById('resNewBtn');
const errMsg = document.getElementById('errMsg');
const errRetryBtn = document.getElementById('errRetryBtn');
if (resDlBtn) {
resDlBtn.addEventListener('click', function() {
setTimeout(() => this.blur(), 100);
});
}
if (resNewBtn) {
resNewBtn.addEventListener('click', function() {
setTimeout(() => this.blur(), 100);
});
}
let selectedFile = null;
let lastBlobUrl = null;
function fmtSize(b) {
if (b < 1024) return b + ' Б';
if (b < 1024 * 1024) return (b / 1024).toFixed(1) + ' КБ';
return (b / 1024 / 1024).toFixed(2) + ' МБ';
}
function setState(name) {
Object.keys(states).forEach(k => {
const el = states[k];
if (!el) return;
el.style.opacity = '0';
el.style.pointerEvents = 'none';
});
const target = states[name];
if (target) { 
target.style.opacity = '1'; 
target.style.pointerEvents = 'all'; 
}
updateFooter(name);
}
function updateFooter(stateName) {
const f = footerElements;
if (f.hint) f.hint.style.display = 'none';
if (f.file) f.file.style.display = 'none';
if (f.consent) f.consent.style.display = 'none';
if (f.runBtn) f.runBtn.style.display = 'none';
if (f.cancelBtn) f.cancelBtn.style.display = 'none';
if (f.resultActions) f.resultActions.style.display = 'none';
if (f.retryBtn) f.retryBtn.style.display = 'none';
if (stateName === 'empty') {
if (f.hint) {
f.hint.style.display = 'block';
f.hint.textContent = 'Файл не обрано';
}
if (f.runBtn) {
f.runBtn.style.display = '';
f.runBtn.disabled = true;
f.runBtn.classList.remove('on');
}
} else if (stateName === 'ready') {
if (f.file) f.file.style.display = '';
if (f.consent) f.consent.style.display = '';
if (f.runBtn) f.runBtn.style.display = '';
} else if (stateName === 'progress') {
if (f.hint) {
f.hint.style.display = 'block';
f.hint.textContent = 'Триває обробка файлу...';
}
if (f.cancelBtn) f.cancelBtn.style.display = '';
} else if (stateName === 'result') {
if (f.resultActions) f.resultActions.style.display = '';
} else if (stateName === 'error') {
if (f.retryBtn) f.retryBtn.style.display = '';
}
}
function setProgress(pct, title) {
if (progFill) progFill.style.width = pct + '%';
if (progPct) progPct.textContent = Math.round(pct) + '%';
if (title && progTitle) progTitle.textContent = title;
}
function setStep(index) {
progSteps.forEach((el, i) => {
if (!el) return;
el.classList.remove('s-active', 's-done');
if (index >= 0) {
if (i < index) el.classList.add('s-done');
else if (i === index) el.classList.add('s-active');
}
});
}
function setFile(file) {
if (!file || !file.name.match(/\.xlsx$/i)) { showError('Оберіть файл формату .xlsx'); return; }
selectedFile = file;
if (readyFileName) readyFileName.textContent = file.name;
if (readyFileSize) readyFileSize.textContent = fmtSize(file.size);
setState('ready');
}
function clearFile() {
selectedFile = null;
if (fileInput) fileInput.value = '';
if (lastBlobUrl) { URL.revokeObjectURL(lastBlobUrl); lastBlobUrl = null; }
const consentCb = document.getElementById('analyzerConsent');
if (consentCb) consentCb.checked = false;
if (readyRunBtn) {
readyRunBtn.disabled = true;
}
setState('empty');
}
function showError(msg) {
if (errMsg) {
const parts = msg.split('\n');
errMsg.innerHTML = parts[0] + (parts[1] ? '<br><small style="opacity:.7">' + parts[1] + '</small>' : '');
}
setState('error');
}
setState('empty');
if (dropZone) {
dropZone.addEventListener('click', () => fileInput && fileInput.click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
dropZone.addEventListener('dragleave', e => { e.preventDefault(); dropZone.classList.remove('drag-over'); });
dropZone.addEventListener('drop', e => {
e.preventDefault(); dropZone.classList.remove('drag-over');
const f = e.dataTransfer.files[0]; if (f) setFile(f);
});
}
if (fileInput) fileInput.addEventListener('change', () => { if (fileInput.files[0]) setFile(fileInput.files[0]); });
if (readyRemove) readyRemove.addEventListener('click', clearFile);
if (resNewBtn) resNewBtn.addEventListener('click', clearFile);
if (errRetryBtn) errRetryBtn.addEventListener('click', clearFile);
if (cancelBtn) cancelBtn.addEventListener('click', () => {
if (window._nszuXhr) { 
window._nszuXhr.abort(); 
window._nszuXhr = null; 
}
clearInterval(window._analyzeTimer);
if (progTitle) progTitle.textContent = 'Скасування...';
setStep(-1); 
setTimeout(() => {
clearFile();
}, 300);
});
if (readyRunBtn) readyRunBtn.addEventListener('click', startAnalysis);
if (consentCb && readyRunBtn) {
consentCb.addEventListener('change', (e) => {
if (e.target.checked) {
readyRunBtn.disabled = false;
readyRunBtn.classList.add('on');
} else {
readyRunBtn.disabled = true;
readyRunBtn.classList.remove('on');
}
});
}
async function startAnalysis() {
if (!selectedFile) return;
if (consentCb && !consentCb.checked) return;
setState('progress');
if (progFill) {
progFill.style.transition = 'none'; progFill.style.width = '0%';
progFill.getBoundingClientRect(); progFill.style.transition = '';
}
if (progPct) progPct.textContent = '0%';
if (progTitle) progTitle.textContent = 'Підготовка...';
setStep(0);
const result = await ExcelAnalyzer.analyzeWithProgress(
selectedFile,
function (stepIndex, pct, label) { setStep(stepIndex); setProgress(pct, label); }
);
if (result.success) {
setStep(5); setProgress(100, 'Готово!');
setTimeout(() => {
const s = result.stats || {};
if (resTotal) resTotal.textContent = s.total != null ? s.total : '—';
if (resMatched) resMatched.textContent = s.matched != null ? s.matched : '—';
if (resSkipped) resSkipped.textContent = s.skipped != null ? s.skipped : '—';
if (resDlBtn && result.blobUrl) {
lastBlobUrl = result.blobUrl; resDlBtn.href = result.blobUrl; resDlBtn.download = result.filename;
}
setState('result');
}, 500);
} else {
if (result.error !== 'Аналіз скасовано') showError(result.error || 'Невідома помилка');
}
}
});
})();