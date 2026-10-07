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
window._modalZTop = 9999;
class ModalManager {
constructor() {
this.tempServicesNotes = null;
this.modal = document.getElementById('modal');
this.searchInput = document.getElementById('search-input');
this.modalList = document.getElementById('modal-list');
this.tabsContainer = document.getElementById('tabs-container');
this.tabContent = document.getElementById('tab-content');
this.tabs = document.getElementById('tabs');
this.iframe = document.getElementById('info-iframe');
this.modalTitle = document.getElementById('modal-title');
this.modalSearchGroup = document.querySelector('.modal-search-group');
this.currentDsgIndex = null;
this.allItems = [];
this.filteredItems = [];
this.visibleCount = 0;
this.batchSize = 50;
this.tabScrollHandler = null;
this.modalStack = [];
this.lastActiveRow = null;
this.initEventListeners();
}
setActiveRow(rowElement) {
if (this.lastActiveRow) {
this.lastActiveRow.classList.remove('row-fade-start', 'row-fade-animate', 'force-hover');
}
this.lastActiveRow = rowElement;
if (rowElement) {
rowElement.classList.add('force-hover');
}
}
saveCurrentState() {
const currentState = {
title: this.modalTitle?.textContent || '',
searchValue: this.searchInput?.value || '',
allItems: [...this.allItems],
filteredItems: [...this.filteredItems],
visibleCount: this.visibleCount,
currentDsgIndex: this.currentDsgIndex,
tempServicesNotes: this.tempServicesNotes,
codeNameMap: this._codeNameMap,
svcCodeNameMap: this._svcCodeNameMap,
activeView: this.getActiveView(),
scrollPosition: this.getScrollPosition()
};
if (this.tabsContainer?.style.display === 'flex') {
const activeTab = document.querySelector('.tab-button.active');
currentState.activeTab = activeTab?.dataset.tab || null;
currentState.tabsData = this.getTabsData();
}
this.modalStack.push(currentState);
}
restorePreviousState() {
if (this.modalStack.length === 0) {
this.closeModal();
return;
}
const previousState = this.modalStack.pop();
const modalContent = this.modal?.querySelector('.modal-content');
const doRestore = () => {
this.hideAllElements();
if (this.modalTitle) this.modalTitle.textContent = previousState.title;
this.allItems = [...previousState.allItems];
this.filteredItems = [...previousState.filteredItems];
this.currentDsgIndex = previousState.currentDsgIndex;
if (previousState.tempServicesNotes !== undefined) this.tempServicesNotes = previousState.tempServicesNotes;
this._codeNameMap = previousState.codeNameMap;
this._svcCodeNameMap = previousState.svcCodeNameMap;
if (this.searchInput) {
this.searchInput.value = previousState.searchValue;
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'flex';
}
if (previousState.activeView === 'list') {
if (this.modalList) {
this.modalList.style.display = 'block';
this.modalList.style.visibility = 'visible';
this.modalList.innerHTML = '';
this.visibleCount = 0;
this.renderBatchFromState(previousState);
setTimeout(() => this.modalList.scrollTop = previousState.scrollPosition, 50);
}
this.setupSearchFromState();
} else if (previousState.activeView === 'tabs') {
if (this.tabsContainer) {
this.tabsContainer.style.display = 'flex';
this.restoreTabsFromState(previousState);
}
}
};
if (modalContent) {
modalContent.classList.add('slide-out-right');
setTimeout(() => {
doRestore();
modalContent.classList.remove('slide-out-right');
modalContent.classList.add('slide-in-left');
setTimeout(() => modalContent.classList.remove('slide-in-left'), 300);
}, 300);
} else {
doRestore();
}
}
renderBatchFromState(state) {
if (!this.modalList) return;
const fragment = document.createDocumentFragment();
state.filteredItems.slice(0, state.visibleCount).forEach(item => {
fragment.appendChild(this.createServiceListItem(item, state.currentDsgIndex));
});
this.modalList.appendChild(fragment);
this.visibleCount = state.visibleCount;
}
setupSearchFromState() {
if (!this.searchInput) return;
this.searchInput.oninput = (e) => {
const val = e.target.value.toLowerCase();
this.filteredItems = val === '' ? [...this.allItems] : this.allItems.filter(i => i.toLowerCase().includes(val));
this.visibleCount = 0;
this.modalList.innerHTML = '';
this.renderBatch();
};
}
getActiveView() {
if (this.tabsContainer?.style.display === 'flex') return 'tabs';
if (this.modalList?.style.display === 'block') return 'list';
if (this.iframe?.style.display === 'block') return 'iframe';
return 'list';
}
getScrollPosition() {
if (this.modalList?.style.display === 'block') return this.modalList.scrollTop;
if (this.tabContent?.scrollTop > 0) return this.tabContent.scrollTop;
return 0;
}
getTabsData() {
const tabsData = {};
document.querySelectorAll('.tab-button').forEach(tab => {
const tabKey = tab.dataset.tab;
const tabContent = document.getElementById(`tab-${tabKey}`);
if (tabContent) {
tabsData[tabKey] = {
description: tab.textContent,
items: Array.from(tabContent.children).map(li => {
if (li.dataset.itemKey) return li.dataset.itemKey;
const textNode = li.firstChild;
return textNode ? textNode.textContent.trim() : li.textContent.trim();
})
};
}
});
return tabsData;
}
restoreTabsFromState(state) {
if (!state.tabsData || !state.activeTab) {
this.closeModal();
return;
}
const dataToUse = (state.originalTabsData && Object.keys(state.originalTabsData).length > 0) ? state.originalTabsData : state.tabsData;
this.tabs.innerHTML = '';
this.tabContent.innerHTML = '';
const keys = Object.keys(dataToUse);
const tabContents = {};
keys.forEach(key => {
const tabBtn = document.createElement('div');
tabBtn.className = 'tab-button';
if (key === state.activeTab) tabBtn.classList.add('active');
tabBtn.textContent = dataToUse[key].description || key;
tabBtn.dataset.tab = key;
this.tabs.appendChild(tabBtn);
const ul = document.createElement('ul');
ul.id = `tab-${key}`;
ul.style.display = key === state.activeTab ? 'block' : 'none';
tabContents[key] = dataToUse[key].items || [];
const currentFilter = state.searchValue ? state.searchValue.toLowerCase() : '';
const itemsToShow = currentFilter ? tabContents[key].filter(item => item.toLowerCase().includes(currentFilter)) : tabContents[key];
const itemsToRender = itemsToShow.slice(0, Math.min(itemsToShow.length, this.batchSize));
itemsToRender.forEach(item => {
ul.appendChild(this.createServiceListItem(item, state.currentDsgIndex));
});
this.tabContent.appendChild(ul);
tabBtn.addEventListener('click', () => {
document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
tabBtn.classList.add('active');
document.querySelectorAll('#tab-content > ul').forEach(ulEl => ulEl.style.display = 'none');
const activeTab = document.getElementById(`tab-${key}`);
if (activeTab) activeTab.style.display = 'block';
if (this.searchInput) this.searchInput.value = '';
this.filterTabContent(key, tabContents[key], '', state.currentDsgIndex);
this.tabContent.scrollTo(0, 0);
});
});
if (this.searchInput) {
this.searchInput.oninput = () => {
const activeTabBtn = document.querySelector('.tab-button.active');
if (activeTabBtn) {
const activeTab = activeTabBtn.dataset.tab;
this.filterTabContent(activeTab, tabContents[activeTab], this.searchInput.value.toLowerCase(), state.currentDsgIndex);
}
};
}
setTimeout(() => this.tabContent.scrollTop = state.scrollPosition, 50);
}
showAdditionalCodesModal(serviceCode, additionalCodes, customTitle = null) {
const title = customTitle || serviceCode;
const codeNameMap = new Map();
const items = [...additionalCodes].sort().map(s => {
const { code, name } = splitCodeName(s);
const key = `${code} ${name}`;
codeNameMap.set(key, { code, name });
return key;
});
const setupContent = () => {
this.hideAllElements();
if (this.modalTitle) this.modalTitle.textContent = title;
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'flex';
if (this.modalList) {
this.modalList.style.display = 'block';
this.modalList.style.visibility = 'visible';
this.modalList.style.minHeight = '100px';
this.modalList.scrollTop = 0;
this.modalList.innerHTML = '';
}
this._codeNameMap = codeNameMap;
this.allItems = items;
this.filteredItems = [...this.allItems];
this.visibleCount = 0;
this.currentDsgIndex = 'code-name-badges';
this.renderBatch();
if (this.searchInput) {
this.searchInput.value = '';
this.searchInput.oninput = (e) => {
const val = e.target.value.toLowerCase();
this.filteredItems = this.allItems.filter(item => item.toLowerCase().includes(val));
this.visibleCount = 0;
this.modalList.innerHTML = '';
this.renderBatch();
};
}
};
if (!this.modal || this.modal.style.display !== 'flex') {
this.openModal();
this.modalStack = [];
setupContent();
return;
}
this.saveCurrentState();
const modalContent = this.modal?.querySelector('.modal-content');
if (modalContent) {
modalContent.classList.add('slide-out-left');
setTimeout(() => {
setupContent();
modalContent.classList.remove('slide-out-left');
modalContent.classList.add('slide-in-right');
setTimeout(() => modalContent.classList.remove('slide-in-right'), 300);
}, 300);
}
}
initEventListeners() {
this.modal?.querySelector('.close-btn')?.addEventListener('click', (e) => {
e.preventDefault();
e.stopPropagation();
this.modalStack.length > 0 ? this.restorePreviousState() : this.closeModal();
});
this.modal?.addEventListener('click', (e) => {
if (e.target === this.modal) {
this.modalStack.length > 0 ? this.restorePreviousState() : this.closeModal();
return;
}
if (e.target.matches('.modal-search-group .clear-btn') && this.searchInput) {
this.searchInput.value = '';
this.searchInput.focus();
this.searchInput.dispatchEvent(new Event('input', { bubbles: true }));
}
});
this.modalList?.addEventListener('scroll', () => this.handleScroll());
document.addEventListener('click', (e) => {
const observationIcon = e.target.closest('.observation-icon');
if (!observationIcon) return;
e.preventDefault();
e.stopPropagation();
observationIcon.classList.add('tooltip-active');
const li = observationIcon.closest('li') || observationIcon.closest('.dsg-row');
if (li) {
window.miniModal.lastActiveRow = li;
li.classList.add('force-hover');
}
setTimeout(() => {
observationIcon.classList.remove('tooltip-active');
try {
const observations = JSON.parse(observationIcon.dataset.observations);
const serviceCode = observationIcon.dataset.serviceCode || 'Невідомо';
App.modalManager.showObservationsModal(observations, serviceCode);
} catch (error) {
console.error('Помилка парсингу observations:', error);
}
}, 10);
});
}
showObservationsModal(observations, serviceCode) {
document.querySelectorAll('.observation-icon.tooltip-active').forEach(icon => {
icon.classList.remove('tooltip-active');
});
const posKey = typeof CF !== 'undefined' && CF.position
? Array.from(CF.position.keys()).find(k => !k.startsWith('__partial__:'))
: null;
const currentPositionCode = posKey?.match(/\(([^)]+)\)$/)?.[1] ?? null;
const filteredObservations = observations.filter(obs => {
if (!obs.position_code_observation || obs.position_code_observation.length === 0) return true;
if (!currentPositionCode) return true;
return obs.position_code_observation.includes(currentPositionCode);
});
const itemsHtml = filteredObservations.map(obs => {
const notesData = {
noteText: obs.additional_requirements || '',
referral: obs.additional_requirements_referral || null,
episodes: [],
additionalCodes: null
};
const iconsHtml = notesSystem.createIconsHtml(notesData, obs.code, true);
let displayText;
if (obs.description && obs.description.trim() !== '' && obs.description !== 'не зазначається') {
displayText = `<strong style="white-space: nowrap;">${esc(obs.code)}&nbsp;-&nbsp;</strong>${esc(obs.description)}`;
} else {
displayText = `<strong style="white-space: nowrap; font-style: italic;">${esc(obs.code)}</strong>`;
}
return `<li>${displayText}${iconsHtml}</li>`;
}).join('');
const modalContent = `<ul id="modal-list">${itemsHtml}</ul>`;
window.showAppendix(`Спостереження | ${serviceCode}`, modalContent);
}
openModal() {
if (!this.modal) return;
if (this.modal.style.display === 'flex') return;
const scrollBarWidth = window.innerWidth - document.documentElement.clientWidth;
this._savedScrollY = window.scrollY;
this.modal.style.zIndex = ++window._modalZTop;
this.modal.classList.remove('show');
this.modal.classList.add('hide');
this.modal.style.display = 'flex';
this.modal.scrollTop = 0;
this.modalList?.scrollTo(0, 0);
this.tabContent?.scrollTo(0, 0);
requestAnimationFrame(() => {
requestAnimationFrame(() => {
if (scrollBarWidth > 0) {
document.body.style.paddingRight = `${scrollBarWidth}px`;
}
document.body.classList.add("modal-open");
this.modal.classList.remove('hide');
this.modal.classList.add('show');
});
});
}
_removeLoader() {
this.modal?.querySelector('.modal-fetch-loader')?.remove();
}
showLoading(title) {
this.modalStack = [];
this.hideAllElements();
this.filteredItems = [];
this.visibleCount = 0;
if (this.modalTitle) this.modalTitle.textContent = title || '';
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'flex';
if (this.modalList) {
this.modalList.style.display = 'block';
this.modalList.style.visibility = 'visible';
this.modalList.style.minHeight = '0';
this.modalList.scrollTop = 0;
this.modalList.innerHTML = '';
const frag = document.createDocumentFragment();
[78, 55, 85, 62, 73, 80, 50, 67].forEach(w => {
const li = document.createElement('li');
li.className = 'modal-skeleton-item';
const bar = document.createElement('div');
bar.className = 'cell-skeleton';
bar.style.width = w + '%';
li.appendChild(bar);
frag.appendChild(li);
});
this.modalList.appendChild(frag);
}
this.openModal();
}
showLoadingTabs(title, tabDefs) {
this.modalStack = [];
this.hideAllElements();
if (this.modalTitle) this.modalTitle.textContent = title || '';
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'flex';
if (this.tabsContainer) this.tabsContainer.style.display = 'flex';
if (!this.tabs || !this.tabContent) { this.openModal(); return; }
if (this.tabContent) this.tabContent.scrollTop = 0;
this.tabs.innerHTML = '';
this.tabContent.innerHTML = '';
tabDefs.forEach((def, index) => {
const tabBtn = document.createElement('div');
tabBtn.className = 'tab-button' + (index === 0 ? ' active' : '');
tabBtn.textContent = def.label;
this.tabs.appendChild(tabBtn);
const ul = document.createElement('ul');
ul.style.display = index === 0 ? 'block' : 'none';
if (index === 0) {
const frag = document.createDocumentFragment();
[78, 55, 85, 62, 73, 80, 50, 67].forEach(w => {
const li = document.createElement('li');
li.className = 'modal-skeleton-item';
const bar = document.createElement('div');
bar.className = 'cell-skeleton';
bar.style.width = w + '%';
li.appendChild(bar);
frag.appendChild(li);
});
ul.appendChild(frag);
}
this.tabContent.appendChild(ul);
});
this.openModal();
}
closeModal() {
if (!this.modal) return;
window.hideActiveTooltip?.();
if (this.lastActiveRow) {
const savedRow = this.lastActiveRow;
this.lastActiveRow = null;
animateRowFade(savedRow);
}
if (!this.lastActiveRow) {
document.querySelectorAll('#modal-list li.force-hover, #tab-content li.force-hover, .body-appendix-modal li.force-hover')
.forEach(li => animateRowFade(li));
}
this.modal.classList.remove('show');
this.modal.classList.add('hide');
setTimeout(() => {
this.modal.style.display = "none";
this.modal.classList.remove('hide');
if (window.miniModal?.layer?.style.display !== 'flex') {
document.body.classList.remove("modal-open");
document.body.style.paddingRight = "";
if (this._savedScrollY !== undefined) {
window.scrollTo(0, this._savedScrollY);
}
}
if (this.searchInput) this.searchInput.value = '';
}, 230);
}
hideAllElements() {
this._removeLoader();
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'none';
if (this.modalList) this.modalList.style.display = 'none';
if (this.tabsContainer) this.tabsContainer.style.display = 'none';
if (this.iframe) this.iframe.style.display = 'none';
const customBody = this.modal?.querySelector('#modal-custom-body');
if (customBody) customBody.style.display = 'none';
const typeDescSlot = document.getElementById('modal-type-desc-slot');
if (typeDescSlot) typeDescSlot.hidden = true;
}
showCustomHtml(title, html, searchFn = null) {
this.hideAllElements();
if (this.modalTitle) this.modalTitle.textContent = title;
let customBody = this.modal?.querySelector('#modal-custom-body');
if (!customBody) {
customBody = document.createElement('div');
customBody.id = 'modal-custom-body';
this.iframe?.insertAdjacentElement('beforebegin', customBody);
}
customBody.innerHTML = html;
customBody.style.display = 'block';
if (searchFn) {
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'flex';
if (this.searchInput) {
this.searchInput.value = '';
this.searchInput.oninput = e => searchFn(e.target.value);
}
}
this.openModal();
}
showListModal(title, items, filterValue = "", dsgIndex = null, overrideAllItems = null) {
this.hideAllElements();
this.currentDsgIndex = dsgIndex;
if (this.modalTitle) this.modalTitle.textContent = title;
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'flex';
if (this.modalList) {
this.modalList.style.display = "block";
this.modalList.style.visibility = "visible";
this.modalList.style.minHeight = "100px";
this.modalList.innerHTML = '';
}
if (this.searchInput) this.searchInput.value = filterValue;
const fullItems = items || [];
this.fullItems = fullItems;
this.allItems = overrideAllItems !== null ? overrideAllItems : fullItems;
this.filteredItems = fullItems.filter(i => i.toLowerCase().includes(filterValue.toLowerCase()));
this.visibleCount = 0;
this.openModal();
requestAnimationFrame(() => {
this.renderBatch();
this.setupSearch(title, dsgIndex);
});
}
showServicesTabs(servicesData, dsgIndex, filterValue = '') {
this.hideAllElements();
this.currentDsgIndex = dsgIndex;
if (this.searchInput) {
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'flex';
this.searchInput.value = filterValue;
}
if (this.tabsContainer) this.tabsContainer.style.display = 'flex';
if (!this.tabs || !this.tabContent) return;
this.tabs.innerHTML = '';
this.tabContent.innerHTML = '';
this.openModal();
requestAnimationFrame(() => {
const keys = Object.keys(servicesData);
const tabContents = {};
keys.forEach((key, index) => {
const tabBtn = document.createElement('div');
tabBtn.className = 'tab-button';
if (index === 0) tabBtn.classList.add('active');
tabBtn.textContent = servicesData[key].description || key;
tabBtn.dataset.tab = key;
this.tabs.appendChild(tabBtn);
const ul = document.createElement('ul');
ul.id = `tab-${key}`;
ul.style.display = index === 0 ? 'block' : 'none';
tabContents[key] = [];
if (Array.isArray(servicesData[key].codes)) {
const initialFiltered = filterValue
? servicesData[key].codes.filter(code => code.toLowerCase().includes(filterValue.toLowerCase()))
: servicesData[key].codes;
this.renderServicesInTab(ul, initialFiltered, 0, dsgIndex);
tabContents[key] = servicesData[key].codes;
}
this.tabContent.appendChild(ul);
tabBtn.addEventListener('click', () => {
document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
tabBtn.classList.add('active');
document.querySelectorAll('#tab-content > ul').forEach(ulEl => ulEl.style.display = 'none');
const activeTab = document.getElementById(`tab-${key}`);
if (activeTab) activeTab.style.display = 'block';
const currentFilter = this.searchInput ? this.searchInput.value.toLowerCase() : '';
this.filterTabContent(key, tabContents[key], currentFilter, dsgIndex);
this.tabContent.scrollTo(0, 0);
});
});
this.setupTabScrolling(tabContents, dsgIndex);
if (this.searchInput) {
this.searchInput.oninput = () => {
const activeTabBtn = document.querySelector('.tab-button.active');
if (activeTabBtn) {
const activeTab = activeTabBtn.dataset.tab;
this.filterTabContent(activeTab, tabContents[activeTab], this.searchInput.value.toLowerCase(), dsgIndex);
}
};
}
});
}
setupTabScrolling(tabContents, dsgIndex) {
if (!this.tabContent) return;
if (this.tabScrollHandler) {
this.tabContent.removeEventListener('scroll', this.tabScrollHandler);
}
this.tabScrollHandler = () => {
const activeTabBtn = document.querySelector('.tab-button.active');
if (!activeTabBtn) return;
const activeTabKey = activeTabBtn.dataset.tab;
const activeTab = document.getElementById(`tab-${activeTabKey}`);
if (!activeTab) return;
const nearBottom = this.tabContent.scrollTop + this.tabContent.clientHeight >= this.tabContent.scrollHeight - 20;
if (nearBottom) {
const currentItems = activeTab.children.length;
const allItems = tabContents[activeTabKey] || [];
if (currentItems < allItems.length) {
this.renderServicesInTab(activeTab, allItems, currentItems, dsgIndex, true);
}
}
};
this.tabContent.addEventListener('scroll', this.tabScrollHandler);
}
renderServicesInTab(ul, services, startIndex, dsgIndex, append = false) {
if (!append) ul.innerHTML = '';
const endIndex = Math.min(startIndex + this.batchSize, services.length);
const fragment = document.createDocumentFragment();
for (let i = startIndex; i < endIndex; i++) {
fragment.appendChild(this.createServiceListItem(services[i], dsgIndex));
}
ul.appendChild(fragment);
}
filterTabContent(tabKey, codes, filterValue = '', dsgIndex) {
const ul = document.getElementById(`tab-${tabKey}`);
if (!ul) return;
const filteredCodes = codes.filter(code => code.toLowerCase().includes(filterValue));
this.renderServicesInTab(ul, filteredCodes, 0, dsgIndex);
}
createServiceListItem(serviceCode, dsgIndex) {
const li = document.createElement('li');
li.dataset.itemKey = serviceCode;
if (dsgIndex === 'all-services' && this._svcCodeNameMap?.has(serviceCode)) {
const { code, name, origKey } = this._svcCodeNameMap.get(serviceCode);
const notesData = resolveServiceNoteData(this.tempServicesNotes?.[origKey]);
const iconsHtml = notesData ? notesSystem.createIconsHtml(notesData, origKey, true) : '';
li.innerHTML = buildPkgListRowHtml(code, name, iconsHtml);
} else if (dsgIndex === 'code-name-badges' && this._codeNameMap?.has(serviceCode)) {
const d = this._codeNameMap.get(serviceCode);
const arPills = (d.ar || []).map(g => `<span class="rehab-ar-pill">${esc(g)}</span>`).join('');
const mainBadge = d.is_main
? '<span class="rehab-main-icon" data-info="' + esc(d.is_main_note ? 'Може бути основним діагнозом: ' + d.is_main_note : 'Може бути основним діагнозом') + '">' + MAIN_DIAG_ICON + '</span>'
: '';
const ageIconsHtml = d.ageScope ? notesSystem.createAgeScopeIconsHtml(d.ageScope, true) : '';
li.innerHTML = buildPkgListRowHtml(d.code, d.name, arPills + mainBadge + ageIconsHtml);
} else {
li.textContent = serviceCode;
}
return li;
}
showDiagnosisTabs(diagnosesData, filterValue = '', initialTab = null) {
this.hideAllElements();
if (this.modalTitle) this.modalTitle.textContent = 'Діагнози';
if (this.searchInput) {
if (this.modalSearchGroup) this.modalSearchGroup.style.display = 'flex';
this.searchInput.value = filterValue;
}
if (this.tabsContainer) this.tabsContainer.style.display = 'flex';
if (!this.tabs || !this.tabContent) return;
this.tabs.innerHTML = '';
this.tabContent.innerHTML = '';
const keys = Object.keys(diagnosesData);
this._codeNameMap = new Map();
keys.forEach(key => {
(diagnosesData[key].codes || []).forEach(s => {
const { code, name } = splitCodeName(s);
this._codeNameMap.set(s, { code, name });
});
});
const STATIC_TAB = keys.find(k => (diagnosesData[k].description || '').indexOf('будь-який') !== -1) || null;
let bestTab = initialTab || keys[0];
let maxMatches = 0;
if (filterValue) {
keys.forEach(key => {
if (key === STATIC_TAB) return;
if (Array.isArray(diagnosesData[key].codes)) {
const matches = diagnosesData[key].codes.filter(code =>
code.toLowerCase().includes(filterValue.toLowerCase())
).length;
if (matches > maxMatches) {
maxMatches = matches;
bestTab = key;
}
}
});
if (maxMatches === 0 && STATIC_TAB !== null) {
bestTab = STATIC_TAB;
filterValue = '';
if (this.searchInput) this.searchInput.value = '';
}
}
this.openModal();
requestAnimationFrame(() => {
const tabContents = {};
keys.forEach(key => {
const tabBtn = document.createElement('div');
tabBtn.className = 'tab-button';
if (key === bestTab) tabBtn.classList.add('active');
tabBtn.textContent = diagnosesData[key].description || key;
tabBtn.dataset.tab = key;
this.tabs.appendChild(tabBtn);
const ul = document.createElement('ul');
ul.id = `tab-${key}`;
ul.style.display = key === bestTab ? 'block' : 'none';
tabContents[key] = [];
if (Array.isArray(diagnosesData[key].codes)) {
const isStatic = key === STATIC_TAB;
const initialFiltered = (filterValue && !isStatic)
? diagnosesData[key].codes.filter(code => code.toLowerCase().includes(filterValue.toLowerCase()))
: diagnosesData[key].codes;
this.renderDiagnosesInTab(ul, initialFiltered, 0);
tabContents[key] = diagnosesData[key].codes;
}
this.tabContent.appendChild(ul);
tabBtn.addEventListener('click', () => {
document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
tabBtn.classList.add('active');
document.querySelectorAll('#tab-content > ul').forEach(ulEl => ulEl.style.display = 'none');
const activeTab = document.getElementById(`tab-${key}`);
if (activeTab) activeTab.style.display = 'block';
const currentFilter = (this.searchInput && key !== STATIC_TAB) ? this.searchInput.value.toLowerCase() : '';
this.filterDiagnosisTabContent(key, tabContents[key], currentFilter);
this.tabContent.scrollTo(0, 0);
});
});
this.setupDiagnosisTabScrolling(tabContents);
if (this.searchInput) {
this.searchInput.oninput = () => {
const val = this.searchInput.value.toLowerCase();
if (val && STATIC_TAB !== null) {
let hasMatch = false;
keys.forEach(key => {
if (key === STATIC_TAB) return;
if (tabContents[key].some(code => code.toLowerCase().includes(val))) hasMatch = true;
});
if (!hasMatch) {
this.searchInput.value = '';
document.querySelectorAll('.tab-button').forEach(btn => {
btn.classList.toggle('active', btn.dataset.tab === STATIC_TAB);
});
document.querySelectorAll('#tab-content > ul').forEach(ulEl => {
ulEl.style.display = ulEl.id === `tab-${STATIC_TAB}` ? 'block' : 'none';
});
this.filterDiagnosisTabContent(STATIC_TAB, tabContents[STATIC_TAB], '');
return;
}
}
const activeTabBtn = document.querySelector('.tab-button.active');
if (activeTabBtn) {
const activeTab = activeTabBtn.dataset.tab;
const filter = activeTab === STATIC_TAB ? '' : val;
this.filterDiagnosisTabContent(activeTab, tabContents[activeTab], filter);
}
};
}
});
}
setupDiagnosisTabScrolling(tabContents) {
if (!this.tabContent) return;
if (this.tabScrollHandler) {
this.tabContent.removeEventListener('scroll', this.tabScrollHandler);
}
this.tabScrollHandler = () => {
const activeTabBtn = document.querySelector('.tab-button.active');
if (!activeTabBtn) return;
const activeTabKey = activeTabBtn.dataset.tab;
const activeTab = document.getElementById(`tab-${activeTabKey}`);
if (!activeTab) return;
const nearBottom = this.tabContent.scrollTop + this.tabContent.clientHeight >= this.tabContent.scrollHeight - 20;
if (nearBottom) {
const currentItems = activeTab.children.length;
const allItems = tabContents[activeTabKey] || [];
if (currentItems < allItems.length) {
this.renderDiagnosesInTab(activeTab, allItems, currentItems, true);
}
}
};
this.tabContent.addEventListener('scroll', this.tabScrollHandler);
}
renderDiagnosesInTab(ul, diagnoses, startIndex, append = false) {
if (!append) ul.innerHTML = '';
const endIndex = Math.min(startIndex + this.batchSize, diagnoses.length);
const fragment = document.createDocumentFragment();
for (let i = startIndex; i < endIndex; i++) {
fragment.appendChild(this.createServiceListItem(diagnoses[i], 'code-name-badges'));
}
ul.appendChild(fragment);
}
filterDiagnosisTabContent(tabKey, codes, filterValue = '') {
const ul = document.getElementById(`tab-${tabKey}`);
if (!ul) return;
const filteredCodes = codes.filter(code => code.toLowerCase().includes(filterValue));
this.renderDiagnosesInTab(ul, filteredCodes, 0);
}
setupSearch(title, dsgIndex) {
if (!this.searchInput) return;
this.searchInput.oninput = (e) => {
const val = e.target.value.toLowerCase();
if (val === '') {
this.filteredItems = [...this.allItems];
} else {
const terms = val.split(/\\+/).map(t => t.trim()).filter(t => t.length > 0);
this.filteredItems = this.allItems.filter(item => {
const itemLower = item.toLowerCase();
return terms.some(term => itemLower.includes(term));
});
}
this.visibleCount = 0;
this.modalList.innerHTML = '';
this.renderBatch();
};
if (this.searchInput.value) {
setTimeout(() => {
this.searchInput.dispatchEvent(new Event('input'));
}, 100);
}
}
handleScroll() {
if (!this.modalList) return;
const nearBottom = this.modalList.scrollTop + this.modalList.clientHeight >= this.modalList.scrollHeight - 20;
if (nearBottom && this.visibleCount < this.filteredItems.length) {
this.renderBatch();
}
}
renderBatch() {
if (!this.modalList) return;
const end = Math.min(this.visibleCount + this.batchSize, this.filteredItems.length);
const fragment = document.createDocumentFragment();
for (let i = this.visibleCount; i < end; i++) {
fragment.appendChild(this.createServiceListItem(this.filteredItems[i], this.currentDsgIndex));
}
this.modalList.appendChild(fragment);
this.visibleCount = end;
}
showIframe(src) {
this.hideAllElements();
if (this.modalTitle) {
this.modalTitle.style.opacity = "0";
this.modalTitle.textContent = "";
}
if (this.iframe) {
this.iframe.style.transition = '';
this.iframe.style.opacity = "0";
this.iframe.style.display = "block";
const modalContent = this.modal?.querySelector('.modal-content');
let loader = document.createElement("div");
loader.className = 'loader modal-loader';
loader.innerHTML = `<div class="spinner"></div>`;
if (modalContent && !modalContent.querySelector(".loader")) {
modalContent.appendChild(loader);
}
this.iframe.src = src;
this.iframe.onload = () => {
const iframeDoc = this.iframe.contentDocument || this.iframe.contentWindow.document;
if (this.modalTitle) {
this.modalTitle.textContent = iframeDoc.title || "Без назви";
this.modalTitle.style.opacity = "1";
}
this.iframe.style.transition = 'opacity 0.2s ease';
this.iframe.style.opacity = "1";
if (loader.parentNode) {
loader.style.transition = 'opacity 0.2s ease';
loader.style.opacity = '0';
setTimeout(() => { if (loader.parentNode) loader.parentNode.removeChild(loader); }, 210);
}
};
this.iframe.onerror = () => {
if (this.modalTitle) {
this.modalTitle.textContent = "Помилка завантаження";
this.modalTitle.style.opacity = "1";
}
if (loader.parentNode) loader.parentNode.removeChild(loader);
};
}
this.openModal();
}
}
function _spawnOverlay(title, content) {
const layer = document.createElement('div');
layer.className = 'appendix-layer appendix-layer--child';
layer.innerHTML = `<div class="appendix-inner">
<span class="close-btn-appendix">&times;</span>
<h3 class="modal-title"></h3>
<div class="body-appendix-modal"></div>
</div>`;
const titleEl = layer.querySelector('.modal-title');
titleEl.textContent = title;
titleEl.style.display = title ? 'block' : 'none';
layer.querySelector('.body-appendix-modal').innerHTML = content;
layer.style.visibility = 'hidden';
document.body.appendChild(layer);
const dismiss = () => {
layer.classList.remove('show');
setTimeout(() => layer.remove(), 200);
};
layer.querySelector('.close-btn-appendix').addEventListener('click', dismiss);
layer.addEventListener('click', e => { if (e.target === layer) dismiss(); });
document.addEventListener('keydown', function escHandler(e) {
if (e.key === 'Escape') {
e.stopImmediatePropagation();
dismiss();
document.removeEventListener('keydown', escHandler);
}
});
layer.style.zIndex = ++window._modalZTop;
layer.style.display = 'flex';
requestAnimationFrame(() => {
void layer.offsetHeight;
layer.style.visibility = '';
requestAnimationFrame(() => layer.classList.add('show'));
});
}
class MiniModal {
constructor() {
this.layer = null;
this.titleElement = null;
this.contentElement = null;
this.lastActiveRow = null;
this._escHandler = (e) => {
if (e.key === 'Escape' && this.isOpen()) {
e.stopImmediatePropagation();
this.close();
}
};
}
_ensureLayer() {
if (this.layer) return true;
const layer = document.createElement('div');
layer.className = 'appendix-layer';
layer.innerHTML = `
<div class="appendix-inner">
<span class="close-btn-appendix">&times;</span>
<h3 class="modal-title"></h3>
<div class="body-appendix-modal"></div>
</div>
`;
document.body.appendChild(layer);
this.layer = layer;
this.titleElement = layer.querySelector('.modal-title');
this.contentElement = layer.querySelector('.body-appendix-modal');
layer.querySelector('.close-btn-appendix').addEventListener('click', () => this.close());
layer.addEventListener('click', (e) => {
if (e.target === layer) this.close();
});
document.addEventListener('keydown', this._escHandler);
return true;
}
show(title = '', content = '') {
this._ensureLayer();
if (window.hideActiveTooltip) window.hideActiveTooltip();
if (!this.lastActiveRow && App.modalManager?.lastActiveRow) {
this.lastActiveRow = App.modalManager.lastActiveRow;
}
if (this.lastActiveRow) {
this.lastActiveRow.classList.add('force-hover');
}
if (this.titleElement) {
this.titleElement.textContent = title;
this.titleElement.style.display = title ? 'block' : 'none';
}
if (this.contentElement) {
this.contentElement.innerHTML = content;
}
const needsScrollLock = !document.body.classList.contains('modal-open');
if (needsScrollLock) this._savedScrollY = window.scrollY;
const scrollBarWidth = needsScrollLock
? window.innerWidth - document.documentElement.clientWidth
: 0;
this.layer.style.zIndex = ++window._modalZTop;
this.layer.style.display = 'flex';
this.layer.scrollTop = 0;
if (this.contentElement) this.contentElement.scrollTop = 0;
requestAnimationFrame(() => {
requestAnimationFrame(() => {
if (needsScrollLock) {
if (scrollBarWidth > 0) {
document.body.style.paddingRight = `${scrollBarWidth}px`;
}
document.body.classList.add('modal-open');
}
this.layer.classList.add('show');
});
});
}
close() {
if (!this.layer) return;
if (this.lastActiveRow) {
const savedRow = this.lastActiveRow;
this.lastActiveRow = null;
animateRowFade(savedRow);
}
this.layer.classList.remove('show');
setTimeout(() => {
if (this.layer) {
this.layer.style.display = 'none';
if (this.contentElement) this.contentElement.scrollTop = 0;
}
if (App.modalManager?.modal?.style.display !== 'flex') {
document.body.style.paddingRight = '';
document.body.classList.remove('modal-open');
if (this._savedScrollY !== undefined) {
window.scrollTo(0, this._savedScrollY);
}
}
}, 200);
}
isOpen() {
return this.layer?.style.display === 'flex';
}
}
let modalManager = null;
function initModalManager() {
if (!modalManager) {
modalManager = new ModalManager();
App.modalManager = modalManager;
}
return modalManager;
}
if (document.readyState === 'loading') {
document.addEventListener('DOMContentLoaded', initModalManager);
} else {
initModalManager();
}
function animateRowFade(row) {
if (!row) return;
row.classList.remove('force-hover');
row.classList.add('row-fade-start');
requestAnimationFrame(() => requestAnimationFrame(() => {
row.classList.remove('row-fade-start');
row.classList.add('row-fade-animate');
setTimeout(() => row.classList.remove('row-fade-animate'), 3000);
}));
}
App.initModalManager = initModalManager;
window.miniModal = new MiniModal();
window.showAppendix = (title, content) => window.miniModal.show(title, content);
window._spawnOverlay = _spawnOverlay;
function warmUpOverlay(el) {
if (!el) return;
const prevVisibility = el.style.visibility;
el.style.visibility = 'hidden';
el.style.display = 'flex';
void el.offsetHeight;
el.style.display = 'none';
el.style.visibility = prevVisibility;
}
function scheduleOverlayWarmUp() {
requestAnimationFrame(() => requestAnimationFrame(() => {
warmUpOverlay(document.getElementById('modal'));
window.miniModal?._ensureLayer();
warmUpOverlay(window.miniModal?.layer);
}));
}
if (document.readyState === 'loading') {
document.addEventListener('DOMContentLoaded', scheduleOverlayWarmUp);
} else {
scheduleOverlayWarmUp();
}
'use strict';
function mkEl(tag, cls) {
var el = document.createElement(tag);
if (cls) el.className = cls;
return el;
}
function esc(s) {
if (s == null) return '';
return String(s)
.replace(/&/g, '&amp;')
.replace(/</g, '&lt;')
.replace(/>/g, '&gt;')
.replace(/"/g, '&quot;');
}
function buildPkgListRowHtml(code, name, metaHtml) {
return '<div class="pkg-list-row">'
+ '<div class="pkg-list-main">'
+ '<span class="pkg-list-code">' + esc(code) + '</span>'
+ '<span class="pkg-list-name">' + esc(name) + '</span>'
+ '</div>'
+ '<div class="pkg-list-meta">' + (metaHtml || '') + '</div>'
+ '</div>';
}
function splitCodeName(s) {
var i = s.indexOf(' - ');
return i === -1 ? { code: s, name: '' } : { code: s.slice(0, i), name: s.slice(i + 3) };
}
function resolveServiceNoteData(notesRaw) {
if (!notesRaw || (Array.isArray(notesRaw) && !notesRaw.length)) return null;
var notes = Array.isArray(notesRaw) ? notesRaw : [notesRaw];
var activePos = typeof CF !== 'undefined'
? Array.from(CF.position.keys()).find(function(k) { return !k.startsWith('__partial__:'); })
: null;
var activePosCode = activePos ? (activePos.match(/\(([^)]+)\)$/) || [])[1] || null : null;
var posMatch = function(p) { return p === activePosCode || p.indexOf('(' + activePosCode + ')') !== -1; };
var n;
if (activePosCode) {
n = notes.find(function(note) { return (note.positions || []).some(posMatch); })
|| notes.find(function(note) { return !(note.positions || []).length; });
if (!n) return null;
} else {
n = notes[0];
}
var buildUnique = function(list) {
var seen = {};
return list.map(function(note) {
return (note.note || '').split('|').map(function(t) { return App.expandRequirementText(t.trim()); }).filter(Boolean).join('<br>—<br>');
}).filter(function(t) { if (!t || seen[t]) return false; seen[t] = true; return true; }).join('<br>—<br>') || null;
};
var noteText;
if (activePosCode) {
var isUniversal = !(n.positions || []).length;
noteText = isUniversal
? buildUnique(notes.filter(function(note) { return !(note.positions || []).length; }))
: (n.note || '').split('|').map(function(t) { return App.expandRequirementText(t.trim()); }).filter(Boolean).join('<br>—<br>') || null;
} else {
noteText = buildUnique(notes);
}
return {
noteText: noteText,
additionalCodes: Array.isArray(n.additionalCodes) ? n.additionalCodes : null,
referral: n.referral || null,
episodes: Array.isArray(n.episodes) ? n.episodes : [],
additionalRequirements: null,
observation_lab: n.observation_lab || null,
observation_gen: n.observation_gen || null
};
}
function toSvcCodeNameItems(codes, mapOut) {
return (codes || []).map(function(s) {
var sp = splitCodeName(s);
var key = sp.code + ' ' + sp.name;
mapOut.set(key, { code: sp.code, name: sp.name, origKey: s });
return key;
});
}
function showCodeNameModal(title, items, filterValue, allItemsPool) {
filterValue = filterValue || '';
var toStr = function(d) { return d.code + ' ' + d.name; };
var displayStrings = (items || []).map(toStr);
var pool = (allItemsPool && allItemsPool.length) ? allItemsPool : items;
var poolStrings = (pool || []).map(toStr);
App.modalManager._codeNameMap = new Map((pool || []).concat(items || []).map(function(d) {
return [toStr(d), d];
}));
App.modalManager.showListModal(title, displayStrings, filterValue, 'code-name-badges', poolStrings);
}
function placeDropdown(marker, panel) {
if (!marker || !panel) return;
panel.style.left = '';
panel.style.right = 'auto';
panel.style.width = panel.style.minWidth = panel.style.maxWidth = '';
panel.classList.remove('open-up');
var vw = document.documentElement.clientWidth;
var pad = 12;
panel.style.maxWidth = (vw - pad * 2) + 'px';
var pr = (panel.offsetParent || marker).getBoundingClientRect();
var mr = marker.getBoundingClientRect();
var pw = panel.getBoundingClientRect().width;
var left = mr.left;
if (left + pw > vw - pad) left = vw - pad - pw;
left = Math.max(pad, left);
panel.style.left = Math.round(left - pr.left) + 'px';
}
function closeAllDropdowns(except) {
document.querySelectorAll('.filter-dropdown-panel, .filter-dropdown-coefficients').forEach(function(p) {
if (p !== except) p.classList.remove('show');
});
document.querySelectorAll('.filter-marker').forEach(function(m) {
var mine = m.querySelector('.filter-dropdown-panel, .filter-dropdown-coefficients');
if (!except || mine !== except) m.classList.remove('active');
});
var st = document.getElementById('service-trigger');
var sm = document.getElementById('service-menu');
if (st) st.classList.remove('active');
if (sm) sm.classList.remove('show');
}
function loadSuggestions(ctx, facetType, q, container, filterType, multiSelect) {
var cacheKey = facetType + ':' + q + ':' + ctx.getKey();
if (ctx.cache[cacheKey]) {
renderSuggestions(ctx.CF, ctx.cache[cacheKey], q, container, filterType, multiSelect);
return;
}
container.innerHTML = '<div style="padding:8px;color:#94a3b8;font-size:13px;">Завантаження...</div>';
ctx.apiCall('facets', { exclude: facetType, q: q })
.then(function(data) {
if (data) ctx.cache[cacheKey] = data;
renderSuggestions(ctx.CF, data, q, container, filterType, multiSelect);
})
.catch(function() {
container.innerHTML = '<div style="padding:8px;color:#ef4444;font-size:13px;">Помилка</div>';
});
}
function renderSuggestions(CF, data, q, container, filterType, multiSelect) {
var sugg = (data && data.suggestions) ? data.suggestions : [];
container.innerHTML = '';
if (q && q.length >= 2) {
var pkey = '__partial__:' + q;
var cfMap = CF[filterType];
var pOpt = mkEl('div', 'dropdown-option dropdown-option-partial');
pOpt.dataset.value = q;
pOpt.dataset.partial = '1';
if (cfMap && cfMap.has(pkey)) pOpt.classList.add('selected');
pOpt.innerHTML = '<span class="option-text">\uD83D\uDDDD\uFE0F <strong>' + esc(q) + '</strong></span>';
container.appendChild(pOpt);
}
if (!sugg.length) {
var empty = mkEl('div');
empty.style.cssText = 'padding:8px;color:#94a3b8;font-size:13px;';
empty.textContent = q ? 'Нічого не знайдено' : 'Введіть для пошуку';
container.appendChild(empty);
return;
}
sugg.forEach(function(s) {
var opt = mkEl('div', 'dropdown-option');
opt.dataset.value = s;
var cfMap = CF[filterType];
var isSel = cfMap && cfMap.has(s);
if (isSel) opt.classList.add('selected');
if (multiSelect) {
opt.appendChild(mkEl('span', 'option-checkbox' + (isSel ? ' checked' : '')));
}
var txt = mkEl('span', 'option-text');
txt.textContent = s;
opt.appendChild(txt);
container.appendChild(opt);
});
}
function initInfiniteScroll(state, loadMoreFn) {
var ticking = false;
var handler = function() {
if (ticking || state.loading || state.offset >= state.total) return;
ticking = true;
requestAnimationFrame(function() {
if (window.scrollY + window.innerHeight >= 
document.documentElement.scrollHeight - 400) loadMoreFn();
ticking = false;
});
};
window.addEventListener('scroll', handler, { passive: true });
return function() { window.removeEventListener('scroll', handler); };
}
const REFERRAL_DOC_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>';
const MAIN_DIAG_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>';
const AR_GROUPS = ['АР1', 'АР2', 'АР3-1', 'АР3-2', 'АР4'];
const DIAG_TYPES = {
'Діагноз_ПП': { short: 'ПП', label: 'Діагноз першопричини' },
'Діагноз_ФО': { short: 'ФО', label: 'Функціональні обмеження' },
'Діагноз_С': { short: 'С', label: 'Статус пацієнта' },
'Діагноз_СП': { short: 'СП', label: 'Симптоми або прояви' },
'Діагноз_СФЗ': { short: 'СФЗ', label: 'Соціально-функціональна залежність' },
};
let INFO = null;
const arFilters = new Set();
const typeFilters = new Set();
let listSearchQuery = '';
let listSearchTimer;
let listController = null;
let listOffset = 0;
let listTotal = 0;
let listLoading = false;
const LIST_PAGE = 50;
let _modalFetchGen = 0;
const listState = {
get offset() { return listOffset; },
get total() { return listTotal; },
get loading() { return listLoading; }
};
const $ = id => document.getElementById(id);
const input = $('rehab-input');
const autocomplete = $('rehab-autocomplete');
const resultTitle = $('rehab-result-title');
const resultGroups = $('rehab-result-groups');
const daggerRow = $('rehab-dagger-row');
const daggerVal = $('rehab-dagger-val');
const typeRow = $('rehab-type-row');
const typeVal = $('rehab-type-val');
const mainRow = $('rehab-main-row');
const mainVal = $('rehab-main-val');
const formulaRow = $('rehab-formula-row');
const formulaVal = $('rehab-formula-val');
const referralRow = $('rehab-referral-row');
const referralVal = $('rehab-referral-val');
const noteRow = $('rehab-note-row');
const noteVal = $('rehab-note-val');
const crRow = $('rehab-cr-row');
const crBadge = $('rehab-cr-badge');
const clearBtn = $('rehab-input-clear');
const arTbody = $('rehab-ar-tbody');
const arTableWrap = document.querySelector('.rehab-ar-table-wrap');
const listWrap = $('rehab-list-wrap');
const listEl = $('rehab-list');
const listTitle = $('rehab-list-title');
const listCount = $('rehab-list-count');
const listSearchInput = $('rehab-list-search');
const listSearchClear = $('rehab-list-search-clear');
const resultPlaceholder = $('rehab-result-placeholder');
async function init() {
try {
const res = await fetch('/serve.php?f=pkg54-info');
INFO = await res.json();
} catch (e) {
console.error('PKG54: не вдалось завантажити info', e);
}
loadList();
bindEvents();
}
function bindEvents() {
input.addEventListener('input', onSearchInput);
input.addEventListener('focus', () => { if (input.value.trim().length >= 1) fetchAutocomplete(input.value.trim()); });
input.addEventListener('keydown', onSearchKeydown);
input.addEventListener('blur', () => setTimeout(() => hideAutocomplete(), 150));
document.querySelectorAll('.rehab-filter-btn[data-ar]').forEach(btn => {
btn.addEventListener('click', () => {
const val = btn.dataset.ar;
if (!val) arFilters.clear();
else if (arFilters.has(val)) arFilters.delete(val);
else arFilters.add(val);
syncFilterButtons('.rehab-filter-btn[data-ar]', 'ar', arFilters);
loadList();
});
});
document.querySelectorAll('.rehab-filter-btn[data-type]').forEach(btn => {
btn.addEventListener('click', () => {
const val = btn.dataset.type;
if (!val) typeFilters.clear();
else if (typeFilters.has(val)) typeFilters.delete(val);
else typeFilters.add(val);
syncFilterButtons('.rehab-filter-btn[data-type]', 'type', typeFilters);
loadList();
});
});
listSearchInput?.addEventListener('input', () => {
listSearchClear.hidden = !listSearchInput.value;
clearTimeout(listSearchTimer);
listSearchTimer = setTimeout(() => {
listSearchQuery = listSearchInput.value.trim();
loadList();
}, 300);
});
listSearchClear?.addEventListener('click', () => {
listSearchInput.value = '';
listSearchClear.hidden = true;
listSearchQuery = '';
loadList();
});
clearBtn.addEventListener('click', () => {
input.value = '';
clearBtn.hidden = true;
hideAutocomplete();
hideResult();
input.focus();
});
document.querySelector('.pmg-action-btn[data-action="cr-rules"]')
?.addEventListener('click', openAllCrRules);
document.getElementById('modal-type-desc-toggle')?.addEventListener('click', () => {
const acc = document.getElementById('modal-type-desc-acc');
const toggle = document.getElementById('modal-type-desc-toggle');
const isOpen = acc.classList.toggle('is-open');
toggle.setAttribute('aria-expanded', String(isOpen));
});
document.addEventListener('click', e => {
if (e.target.closest('.rehab-dagger-badge')) openDaggerInfo();
});
}
let searchTimer;
let acItems = [];
let acIndex = -1;
let acController = null;
function onSearchInput() {
clearBtn.hidden = !input.value;
clearTimeout(searchTimer);
const q = input.value.trim();
if (q.length < 1) {
hideAutocomplete();
if (!q) hideResult();
return;
}
searchTimer = setTimeout(() => fetchAutocomplete(q), 220);
}
async function fetchAutocomplete(q) {
if (acController) acController.abort();
acController = new AbortController();
const params = new URLSearchParams({ q, limit: 20 });
try {
const res = await fetch('/serve.php?f=pkg54-search&' + params, { signal: acController.signal });
const data = await res.json();
acItems = data.rows || [];
acIndex = -1;
renderAutocomplete();
} catch (e) { if (e.name !== 'AbortError') console.error(e); }
}
function renderAutocomplete() {
if (!acItems.length) { hideAutocomplete(); return; }
autocomplete.innerHTML = acItems.map((d, i) => `
<div class="rehab-ac-item ${i === acIndex ? 'active' : ''}" data-code="${esc(d.code)}" role="option">
<span class="rehab-ac-code">${esc(d.code)}</span>
<span class="rehab-ac-name">${esc(d.name)}</span>
${d.ar.length ? '<span class="rehab-ac-ar">' + d.ar.map(esc).join(', ') + '</span>' : ''}
</div>
`).join('');
autocomplete.querySelectorAll('.rehab-ac-item').forEach((el, i) => {
el.addEventListener('mousedown', () => selectCode(acItems[i].code, acItems[i].name));
});
autocomplete.hidden = false;
}
function hideAutocomplete() {
autocomplete.hidden = true;
acItems = [];
acIndex = -1;
}
function onSearchKeydown(e) {
if (autocomplete.hidden) return;
if (e.key === 'ArrowDown') { e.preventDefault(); acIndex = Math.min(acIndex + 1, acItems.length - 1); renderAutocomplete(); }
if (e.key === 'ArrowUp') { e.preventDefault(); acIndex = Math.max(acIndex - 1, -1); renderAutocomplete(); }
if (e.key === 'Enter' && acIndex >= 0) { e.preventDefault(); selectCode(acItems[acIndex].code, acItems[acIndex].name); }
if (e.key === 'Escape') hideAutocomplete();
}
function selectCode(code, name) {
input.value = name ? `${code} ${name}` : code;
clearBtn.hidden = false;
hideAutocomplete();
fetchAndShowResult(code);
}
async function fetchAndShowResult(code) {
try {
const res = await fetch('/serve.php?f=pkg54-diag&code=' + encodeURIComponent(code.toUpperCase()));
if (!res.ok) { hideResult(); return; }
const d = await res.json();
showResult(d);
} catch (e) { console.error(e); }
}
function buildMainHtml(entries, e0) {
if (entries.length === 0 || e0.is_main == null) return null;
const mainDiffers = entries.length > 1 && entries.some(e => e.is_main !== e0.is_main);
if (mainDiffers) {
return entries.map(e => {
const note = e.is_main_note ? '<span class="rehab-main-note">' + esc(e.is_main_note) + '</span>' : '';
return '<div class="rehab-entry-block">'
+ '<span class="rehab-entry-type-tag">' + esc(e.type) + '</span>'
+ (e.is_main ? '<span class="rehab-yes">Так</span>' + note : '<span class="rehab-no">Ні</span>')
+ '</div>';
}).join('');
}
const note = e0.is_main_note ? '<span class="rehab-main-note">' + esc(e0.is_main_note) + '</span>' : '';
return e0.is_main
? '<span class="rehab-yes">Так</span>' + note
: '<span class="rehab-no">Ні</span>';
}
function buildReferralHtml(entries, e0ref) {
if (entries.length === 0) return null;
const referralDiffers = entries.length > 1 && entries.some(e => e.referral_pmd !== e0ref.referral_pmd);
if (referralDiffers) {
return entries.map(e =>
`<div class="rehab-entry-block">
<span class="rehab-entry-type-tag">${esc(e.type)}</span>
${e.referral_pmd ? '<span class="rehab-yes">Так</span>' : '<span class="rehab-no">Ні</span>'}
</div>`
).join('');
}
return e0ref.referral_pmd
? '<span class="rehab-yes">Так</span>'
: '<span class="rehab-no">Ні</span>';
}
function buildFormulaHtml(entries) {
const entriesWithFormula = entries.filter(e => e.formula);
if (!entriesWithFormula.length) return null;
const formulasDiffer = entriesWithFormula.length > 1
&& entriesWithFormula.some(e => e.formula !== entriesWithFormula[0].formula);
return formulasDiffer
? entriesWithFormula.map(e =>
`<div class="rehab-entry-block">
<span class="rehab-entry-type-tag">${esc(e.type)}</span>
<span class="rehab-entry-formula">${formulaWithButtons(e.formula)}</span>
</div>`
).join('')
: formulaWithButtons(entriesWithFormula[0].formula);
}
function buildArTableRows(entries, ar_info) {
return AR_GROUPS.map(ar => {
const arEntries = entries.filter(e => (e.ar || []).includes(ar));
const info = (ar_info || {})[ar];
if (!arEntries.length) {
return `<tr class="rehab-ar-row rehab-ar-row--disabled">
<td><span class="rehab-ar-label disabled">${esc(ar)}</span></td>
<td colspan="5"><span class="rehab-dash">—</span></td>
</tr>`;
}
const fullDuration = info && info.duration ? info.duration : '';
const duration = esc((info && info.duration_short) || fullDuration || '—');
const durationTooltip = fullDuration ? ` data-info="${esc(fullDuration)}"` : '';
const coefficient = info && info.coeff != null
? esc(String(info.coeff).replace('.', ','))
: '—';
const rate = Number(INFO && INFO.rate);
const coefficientValue = Number(info && info.coeff);
const payment = rate > 0 && Number.isFinite(coefficientValue)
? new Intl.NumberFormat('uk-UA', { maximumFractionDigits: 2 }).format(rate * coefficientValue)
: '—';
const episode = esc((info && info.episode) || '—');
const treatmentPlan = esc((info && info.plan) || '—');
return `<tr class="rehab-ar-row">
<td><span class="rehab-ar-label">${esc(ar)}</span></td>
<td class="rehab-coeff">${coefficient}</td>
<td class="rehab-payment">${payment}</td>
<td class="rehab-duration"${durationTooltip}>${duration}</td>
<td class="rehab-episode">${episode}</td>
<td class="rehab-treatment-plan">${treatmentPlan}</td>
</tr>`;
}).join('');
}
function showResult(d) {
resultTitle.textContent = `${d.code} ${d.name}`;
resultGroups.innerHTML = d.ar.length
? d.ar.map(g => `<span class="rehab-ar-pill">${esc(g)}</span>`).join(' ')
: '<span class="rehab-no-ar">Не входить до жодної групи АР</span>';
if (d.marker) {
daggerRow.hidden = false;
daggerVal.innerHTML = `<span class="rehab-dagger-badge">${esc(d.marker)}</span>`;
} else {
daggerRow.hidden = true;
}
if (d.note) {
noteRow.hidden = false;
noteVal.textContent = d.note;
} else {
noteRow.hidden = true;
}
const entries = d.entries || [];
if (entries.length) {
typeRow.hidden = false;
typeVal.innerHTML = entries.map(e => {
const cls = `rehab-type-${e.type.replace('Діагноз_', '').toLowerCase()}`;
return `<span class="rehab-type-pill ${cls} rehab-type-pill--clickable" data-type="${esc(e.type)}">${esc(e.type)}</span>`;
}).join(' ');
typeVal.querySelectorAll('.rehab-type-pill--clickable').forEach(el => {
el.addEventListener('click', () => openTypeDescInfo(el.dataset.type));
});
} else {
typeRow.hidden = true;
}
const e0ref = entries[0] || {};
const mainHtml = buildMainHtml(entries, e0ref);
if (mainHtml !== null) {
mainRow.hidden = false;
mainVal.innerHTML = mainHtml;
} else {
mainRow.hidden = true;
}
const formulaHtml = buildFormulaHtml(entries);
if (formulaHtml !== null) {
formulaRow.hidden = false;
formulaVal.innerHTML = formulaHtml;
formulaVal.querySelectorAll('.rehab-type-btn').forEach(btn => {
btn.addEventListener('click', () => openTypeModal(btn.dataset.type));
});
} else {
formulaRow.hidden = true;
}
const referralHtml = buildReferralHtml(entries, e0ref);
if (referralHtml !== null) {
referralRow.hidden = false;
referralVal.innerHTML = referralHtml;
} else {
referralRow.hidden = true;
}
if (d.cr_code && d.cr_detail) {
crRow.hidden = false;
crBadge.textContent = `${d.cr_code} – ${d.cr_detail.group}`;
crBadge.onclick = () => openCrModal(d.cr_code, d.cr_detail);
} else {
crRow.hidden = true;
}
arTableWrap.hidden = false;
renderArTable(d);
resultTitle.hidden = false;
resultPlaceholder.hidden = true;
}
function formulaWithButtons(formula) {
const pattern = Object.keys(DIAG_TYPES)
.sort((a, b) => b.length - a.length)
.join('|');
const re = new RegExp(pattern, 'g');
let result = '';
let last = 0;
let m;
while ((m = re.exec(formula)) !== null) {
result += esc(formula.slice(last, m.index));
result += `<button class="rehab-type-btn" data-type="${esc(m[0])}" type="button">${esc(m[0])}</button>`;
last = re.lastIndex;
}
result += esc(formula.slice(last));
return result;
}
function renderArTable(d) {
arTbody.innerHTML = buildArTableRows(d.entries || [], d.ar_info);
arTbody.querySelectorAll('.rehab-type-btn').forEach(btn => {
btn.addEventListener('click', () => openTypeModal(btn.dataset.type));
});
}
function resetList() {
listOffset = 0;
listTotal = 0;
listEl.innerHTML = '';
}
function showListSkeleton(count) {
const widths = [70, 50, 85, 60, 75, 55, 90, 65, 72, 88, 58, 78];
listEl.innerHTML = Array.from({ length: count }, (_, i) => {
const w = widths[i % widths.length];
return `<div class="rehab-list-row rehab-list-row--skeleton">
<div class="rehab-list-main">
<div class="cell-skeleton" style="width:${Math.round(w * 0.28)}%;margin-right:8px;flex-shrink:0"></div>
<div class="cell-skeleton" style="width:${w}%"></div>
</div>
<div class="rehab-list-meta">
<div class="cell-skeleton cell-skeleton-sm" style="width:40px;height:18px;border-radius:10px"></div>
</div>
</div>`;
}).join('');
listWrap.hidden = false;
}
async function loadList(append = false) {
if (append && listLoading) return;
if (listController) listController.abort();
listController = new AbortController();
if (!append) {
const skelCount = Math.min(listOffset || LIST_PAGE, LIST_PAGE);
resetList();
showListSkeleton(skelCount);
}
listLoading = true;
const params = new URLSearchParams({ limit: LIST_PAGE, offset: listOffset });
arFilters.forEach(ar => params.append('ar', ar));
typeFilters.forEach(t => params.append('type', t));
if (listSearchQuery) params.set('q', listSearchQuery);
try {
const res = await fetch('/serve.php?f=pkg54-search&' + params, { signal: listController.signal });
const data = await res.json();
listTotal = data.total;
listOffset += data.rows.length;
if (!append) listEl.innerHTML = '';
updateListTitle();
listCount.textContent = `(${listTotal})`;
data.rows.forEach(d => {
const row = document.createElement('div');
row.className = 'rehab-list-row';
const arPills = d.ar.length
? d.ar.map(g => `<span class="rehab-ar-pill">${esc(g)}</span>`).join('')
: '';
const typePill = (d.types || [d.type]).filter(Boolean).map(t =>
DIAG_TYPES[t]
? `<span class="rehab-type-pill rehab-type-${t.replace('Діагноз_', '').toLowerCase()}">${esc(t)}</span>`
: ''
).join('');
const crBadgeHtml = d.cr_code
? `<button type="button" class="rehab-cr-badge-sm">${esc(d.cr_code)} – ${esc(d.cr_group || '')}</button>`
: '';
const mainBadge = d.is_main
? '<span class="rehab-main-icon" data-info="' + esc(d.is_main_note ? 'Може бути основним діагнозом: ' + d.is_main_note : 'Може бути основним діагнозом') + '">' + MAIN_DIAG_ICON + '</span>'
: '';
const noteBadge = d.note
? '<span class="rehab-note-badge" data-info="' + esc(d.note) + '">Примітка</span>'
: '';
const refIcon = d.referral_pmd === true
? '<span class="rehab-referral-icon rehab-referral-icon--yes" data-info="Направлення лікаря ПМД на монопослугу: Так">' + REFERRAL_DOC_ICON + '</span>'
: d.referral_pmd === false
? '<span class="rehab-referral-icon rehab-referral-icon--no" data-info="Направлення лікаря ПМД на монопослугу: Ні">' + REFERRAL_DOC_ICON + '</span>'
: d.referral_pmd === null
? '<span class="rehab-referral-icon rehab-referral-icon--mixed" data-info="Направлення лікаря ПМД на монопослугу залежить від типу діагнозу — див. картку">' + REFERRAL_DOC_ICON + '</span>'
: '';
row.innerHTML = `
<div class="rehab-list-main">
<button class="rehab-list-code" data-code="${esc(d.code)}" type="button">${esc(d.code)}</button>
<span class="rehab-list-name">${esc(d.name)}</span>
</div>
<div class="rehab-list-meta">
${arPills}${typePill}${crBadgeHtml}${noteBadge}${mainBadge}${refIcon}
</div>
`;
row.querySelector('.rehab-list-code').addEventListener('click', () => {
showDiagInModal(d.code, d.name);
});
const crBtn = row.querySelector('.rehab-cr-badge-sm');
if (crBtn) {
crBtn.addEventListener('click', () => {
const crDetail = INFO?.cr_rules?.[d.cr_code];
if (crDetail) openCrModal(d.cr_code, crDetail);
});
}
listEl.appendChild(row);
});
if (listTotal === 0) {
const sub = listSearchQuery
? 'Спробуйте змінити пошуковий запит або скинути фільтри'
: 'Спробуйте змінити або скинути фільтри';
listEl.innerHTML = `
<div class="empty-message" style="display:block">
<div class="empty-message-inner">
<svg class="empty-message-icon" viewBox="0 0 72 72" fill="none">
<circle cx="31" cy="31" r="18" stroke="currentColor" stroke-width="3.5"/>
<line x1="44" y1="44" x2="58" y2="58" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/>
<line x1="23" y1="31" x2="39" y2="31" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
</svg>
<p class="empty-message-title">Нічого не знайдено</p>
<p class="empty-message-sub">${sub}</p>
</div>
</div>`;
}
listWrap.hidden = false;
} catch (e) { if (e.name !== 'AbortError') console.error(e); }
finally { listLoading = false; }
}
function updateListTitle() {
const ars = [...arFilters];
const types = [...typeFilters];
if (!ars.length && !types.length) {
listTitle.textContent = 'Всі діагнози';
return;
}
const parts = [];
if (ars.length) parts.push(ars.join(', '));
if (types.length) parts.push(types.map(t => { const s = DIAG_TYPES[t]?.short || t.replace('Діагноз_', ''); return 'Діагнози_' + s; }).join(', '));
listTitle.textContent = parts.join(' · ');
}
function syncFilterButtons(selector, dataKey, activeSet) {
document.querySelectorAll(selector).forEach(b => {
const v = b.dataset[dataKey];
b.classList.toggle('active', !v ? activeSet.size === 0 : activeSet.has(v));
});
}
function hideResult() {
resultPlaceholder.hidden = false;
resultTitle.hidden = true;
resultGroups.innerHTML = '';
[daggerRow, noteRow, typeRow, mainRow, formulaRow, referralRow, crRow].forEach(r => { r.hidden = true; });
arTableWrap.hidden = true;
}
async function openTypeModal(typeKey) {
const info = DIAG_TYPES[typeKey] || { short: typeKey, label: typeKey };
const title = `Діагнози_${info.short} – ${info.label}`;
const desc = INFO?.diag_types?.[typeKey]?.desc || '';
App.modalManager.showLoading(title);
const gen = ++_modalFetchGen;
try {
const res = await fetch('/serve.php?f=pkg54-type-list&type=' + encodeURIComponent(typeKey));
const data = await res.json();
if (gen !== _modalFetchGen) return;
showCodeNameModal(title, data.rows || []);
const slot = document.getElementById('modal-type-desc-slot');
const descBody = document.getElementById('modal-type-desc-body');
const descToggle = document.getElementById('modal-type-desc-toggle');
const acc = document.getElementById('modal-type-desc-acc');
if (descBody) descBody.textContent = desc;
if (acc) acc.classList.remove('is-open');
if (descToggle) descToggle.setAttribute('aria-expanded', 'false');
if (slot) slot.hidden = !desc;
} catch (e) {
console.error(e);
}
}
function openTypeDescInfo(typeKey) {
const info = DIAG_TYPES[typeKey] || { short: typeKey, label: typeKey };
const desc = INFO?.diag_types?.[typeKey]?.desc || '';
if (!desc) return;
const title = `Діагнози_${info.short} – ${info.label}`;
const html = `<p class="rehab-type-desc">${esc(desc)}</p>`;
if (window.miniModal?.isOpen()) {
window._spawnOverlay(title, html);
} else {
window.showAppendix(title, html);
}
}
function openDaggerInfo() {
const info = INFO?.dagger_info;
if (!info?.desc) return;
const title = info.title || 'Хрестик / зірочка';
const html = `<p class="rehab-type-desc">${esc(info.desc)}</p>`;
if (window.miniModal?.isOpen()) {
window._spawnOverlay(title, html);
} else {
window.showAppendix(title, html);
}
}
function openAllCrRules() {
if (!INFO?.cr_rules) return;
const entries = Object.entries(INFO.cr_rules);
const accordionItems = entries.map(([code, d]) => {
const examples = (d.examples || [])
.map(ex => `<div class="rehab-cr-example">${esc(ex)}</div>`)
.join('');
const examplesText = (d.examples || []).join(' ');
return `<div class="accordion-item cr-rule-item" data-code="${esc(code)}" data-title="${esc(d.group)}" data-rule="${esc(d.rule)}" data-examples="${esc(examplesText)}">
<button class="accordion-header" aria-expanded="false" type="button">
<span class="acc-badge">${esc(code)}</span>
<span class="acc-title">${esc(d.group)}</span>
<svg class="acc-chevron" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>
</button>
<div class="accordion-body">
<div class="accordion-content">
<p class="rehab-type-desc">${esc(d.rule)}</p>
${examples ? `<p class="rehab-cr-examples-title">Приклади кодування</p>${examples}` : ''}
</div>
</div>
</div>`;
}).join('');
App.modalManager.showCustomHtml(
'Правила CR',
`<div class="accordion pmg-accordion" id="cr-rules-accordion">${accordionItems}</div>`,
q => {
const lq = q.toLowerCase();
document.querySelectorAll('#cr-rules-accordion .cr-rule-item').forEach(item => {
item.hidden = q
? !item.dataset.code.toLowerCase().includes(lq) &&
!item.dataset.title.toLowerCase().includes(lq) &&
!item.dataset.rule.toLowerCase().includes(lq) &&
!item.dataset.examples.toLowerCase().includes(lq)
: false;
});
}
);
document.querySelectorAll('#cr-rules-accordion .accordion-header').forEach(btn => {
btn.addEventListener('click', () => {
const expanded = btn.getAttribute('aria-expanded') === 'true';
const body = btn.nextElementSibling;
btn.setAttribute('aria-expanded', String(!expanded));
body.style.maxHeight = expanded ? '0' : body.scrollHeight + 'px';
});
});
}
// Модалка: одне CR правило
function openCrModal(crCode, crDetail) {
const examples = (crDetail.examples || [])
.map(ex => `<div class="rehab-cr-example">${esc(ex)}</div>`)
.join('');
App.modalManager.showCustomHtml(
`${crCode} – ${crDetail.group}`,
`<p class="rehab-type-desc">${esc(crDetail.rule)}</p>${examples ? `<p class="rehab-cr-examples-title">Приклади кодування</p>${examples}` : ''}`
);
}
function buildDiagModalHtml(d) {
const entries = d.entries || [];
const e0 = entries[0] || {};
const groupsHtml = d.ar.length
? d.ar.map(g => `<span class="rehab-ar-pill">${esc(g)}</span>`).join(' ')
: '<span class="rehab-no-ar">Не входить до жодної групи АР</span>';
const typeHtml = entries.map(e => {
const cls = `rehab-type-${e.type.replace('Діагноз_', '').toLowerCase()}`;
return `<span class="rehab-type-pill ${cls} rehab-type-pill--clickable" data-type="${esc(e.type)}">${esc(e.type)}</span>`;
}).join(' ');
const mainHtml = buildMainHtml(entries, e0);
const formulaHtml = buildFormulaHtml(entries);
const referralHtml = buildReferralHtml(entries, e0);
const crHtml = (d.cr_code && d.cr_detail)
? `<button class="rehab-cr-badge rehab-cr-badge--modal" type="button">${esc(d.cr_code)} – ${esc(d.cr_detail.group)}</button>`
: '';
const tableRows = buildArTableRows(entries, d.ar_info);
return `
<div class="rehab-info-row" style="border-top:none">
<span class="rehab-info-key">Група АР</span>
<div class="rehab-info-val rehab-modal-card-groups">${groupsHtml}</div>
</div>
${d.marker ? `<div class="rehab-info-row"><span class="rehab-info-key">Хрестик / зірочка</span><div class="rehab-info-val"><span class="rehab-dagger-badge">${esc(d.marker)}</span></div></div>` : ''}
${typeHtml ? `<div class="rehab-info-row"><span class="rehab-info-key">Тип діагнозу</span><div class="rehab-info-val">${typeHtml}</div></div>` : ''}
${mainHtml ? `<div class="rehab-info-row"><span class="rehab-info-key">Основний діагноз</span><div class="rehab-info-val">${mainHtml}</div></div>` : ''}
${formulaHtml ? `<div class="rehab-info-row"><span class="rehab-info-key">Формула кодування</span><div class="rehab-info-val">${formulaHtml}</div></div>` : ''}
${referralHtml ? `<div class="rehab-info-row"><span class="rehab-info-key">Направлення лікаря ПМД на монопослугу</span><div class="rehab-info-val">${referralHtml}</div></div>` : ''}
${d.note ? `<div class="rehab-info-row rehab-note-row"><span class="rehab-info-key">Примітка</span><div class="rehab-info-val">${esc(d.note)}</div></div>` : ''}
${crHtml ? `<div class="rehab-info-row"><span class="rehab-info-key">Правило CR</span><div class="rehab-info-val">${crHtml}</div></div>` : ''}
<div class="rehab-ar-table-wrap" style="margin-top:12px">
<table class="rehab-ar-table">
<thead><tr><th>АР</th><th>Коеф.</th><th>Роз. оплата, грн</th><th>Тривалість</th><th>Епізод</th><th>План лікування</th></tr></thead>
<tbody>${tableRows}</tbody>
</table>
</div>
`;
}
async function showDiagInModal(code, name) {
window.miniModal.show(code + (name ? ' – ' + name : ''), '<p style="color:#94a3b8;font-size:13px;padding:4px 0">Завантаження...</p>');
const gen = ++_modalFetchGen;
try {
const res = await fetch('/serve.php?f=pkg54-diag&code=' + encodeURIComponent(code.toUpperCase()));
if (gen !== _modalFetchGen) return;
if (!res.ok) { window.miniModal.close(); return; }
const d = await res.json();
if (gen !== _modalFetchGen) return;
window.miniModal.show(d.code + ' ' + d.name, buildDiagModalHtml(d));
document.querySelectorAll('.body-appendix-modal .rehab-type-btn').forEach(btn => {
btn.addEventListener('click', () => openTypeModal(btn.dataset.type));
});
document.querySelectorAll('.body-appendix-modal .rehab-type-pill--clickable').forEach(el => {
el.addEventListener('click', () => openTypeDescInfo(el.dataset.type));
});
const crModalBtn = document.querySelector('.body-appendix-modal .rehab-cr-badge--modal');
if (crModalBtn) crModalBtn.addEventListener('click', () => openCrModal(d.cr_code, d.cr_detail));
} catch (e) { console.error(e); window.miniModal.close(); }
}
// esc() — спільна утиліта з pkg-ui.js (входить у цей же бандл)
// Старт
document.addEventListener('DOMContentLoaded', () => {
if (!document.getElementById('rehab-input')) return;
init();
initInfiniteScroll(listState, () => loadList(true));
if (window.initScrollToTop) window.initScrollToTop();
});