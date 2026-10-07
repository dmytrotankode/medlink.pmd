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
const PKG = {
package: (typeof dsgData !== 'undefined') ? dsgData.currentPackage : '47',
offset: 0, limit: 20, total: 0, sort: '',
extra_cols: false,
meta: { RATE: 0, COEFF: 0 },
filters: {
dsg_ex: [], dsg_pa: [],
diag_ex: [], diag_pa: [],
svc_ex: [], svc_pa: [],
coeffs: [],
},
};
const CF = {
dsg: new Map(),
diagnosis: new Map(),
service: new Map(),
coeffs: new Set(),
};
var _facetsCache = {};
var _abortCtrl = null;
var _abortCtrlFacets = null;
var _loadGen = 0;
var _loadMoreActive = false;
var _uiCtx = {
cache: _facetsCache,
getKey: getFiltersKey,
apiCall: apiCall,
CF: CF
};
function getFiltersKey() {
return JSON.stringify(PKG.filters);
}
function invalidateFacetsCache() {
for (var k in _facetsCache) delete _facetsCache[k];
}
document.addEventListener('DOMContentLoaded', async function () {
var cont = document.getElementById('dsg-table-container');
if (typeof App !== 'undefined' && App.notesSystem) {
await App.notesSystem.initialize();
}
initCompactFilters();
initCoeffFilter();
initClearAll();
initInfiniteScroll(PKG, function() { loadRows(true); });
if (typeof window.initScrollToTop === 'function') {
window.initScrollToTop();
var scrollBtn = document.getElementById('scrollToTop');
if (scrollBtn) scrollBtn.style.display = window.scrollY > 300 ? 'block' : 'none';
}
if (typeof window.showCoeffDetails !== 'function') {
window.showCoeffDetails = function () {
if (typeof App !== 'undefined' && App.modalManager) {
App.modalManager.showIframe('/serve.php?f=coeff-details&package=' + PKG.package);
}
};
}
await loadRows(false);
});
function apiCall(action, extra) {
var signal;
if (action === 'search') {
if (_abortCtrl) _abortCtrl.abort();
_abortCtrl = new AbortController();
signal = _abortCtrl.signal;
} else if (action === 'facets') {
if (_abortCtrlFacets) _abortCtrlFacets.abort();
_abortCtrlFacets = new AbortController();
signal = _abortCtrlFacets.signal;
}
var params = Object.assign({
f: 'pkg-search', package: PKG.package, action,
dsg_ex: JSON.stringify(PKG.filters.dsg_ex),
dsg_pa: JSON.stringify(PKG.filters.dsg_pa),
diag_ex: JSON.stringify(PKG.filters.diag_ex),
diag_pa: JSON.stringify(PKG.filters.diag_pa),
svc_ex: JSON.stringify(PKG.filters.svc_ex),
svc_pa: JSON.stringify(PKG.filters.svc_pa),
coeffs: JSON.stringify(PKG.filters.coeffs),
}, extra || {});
return fetch('/serve.php?' + new URLSearchParams(params), { signal: signal })
.then(function(r) {
if (!r.ok) throw new Error('HTTP ' + r.status);
return r.json();
})
.catch(function(err) {
if (err.name === 'AbortError') return null;
throw err;
});
}
function loadRows(append) {
var cont = document.getElementById('dsg-table-container');
if (!cont) return Promise.resolve();
if (append) {
if (_loadMoreActive || PKG.offset >= PKG.total) return;
_loadMoreActive = true;
var genSnapshot = _loadGen;
var offsetSnapshot = PKG.offset;
apiCall('search', { offset: String(offsetSnapshot), limit: String(PKG.limit), sort: PKG.sort })
.then(function(data) {
if (genSnapshot !== _loadGen) return;
if (!data || !data.rows.length) return;
var tbody = cont.querySelector('.dsg-tbody');
if (tbody) { renderRows(data.rows, tbody, true); PKG.offset = offsetSnapshot + data.rows.length; }
})
.catch(function(e) { if (e && e.name !== 'AbortError') console.error('PKG loadMore error:', e); })
.finally(function() { _loadMoreActive = false; });
return;
}
if (_abortCtrl) _abortCtrl.abort();
var gen = ++_loadGen;
var skelCount = Math.min(PKG.offset || PKG.limit, PKG.limit);
PKG.offset = 0;
var skelTbody = buildTableShell(cont);
buildSkeletonRows(skelTbody, skelCount);
cont.classList.add('table-is-loading', 'visible');
return apiCall('search', { offset: '0', limit: String(PKG.limit), sort: PKG.sort })
.then(function(data) {
if (gen !== _loadGen || !data) return;
PKG.total = data.total;
if (data.meta) {
PKG.meta = data.meta;
if (data.meta.extra_cols !== undefined) PKG.extra_cols = data.meta.extra_cols;
renderMeta(data.meta);
}
var tbody = buildTableShell(cont);
if (!data.rows || !data.rows.length) {
App.showEmptyTableState('Збігів не знайдено');
cont.classList.remove('table-is-loading');
return;
}
App.hideEmptyTableState();
renderRows(data.rows, tbody, false);
PKG.offset = data.rows.length;
cont.classList.remove('table-is-loading', 'visible');
requestAnimationFrame(function() { cont.classList.add('visible'); });
})
.catch(function(e) {
if (e && e.name === 'AbortError') return;
console.error('PKG error:', e);
if (gen === _loadGen) {
App.showEmptyTableState('Не вдалося завантажити дані. Перевірте з\'єднання та оновіть сторінку.');
cont.classList.remove('table-is-loading');
}
})
.finally(function() { if (gen === _loadGen) cont.classList.remove('table-is-loading'); });
}
function renderRows(rows, tbody, append) {
if (!append) { while (tbody.firstChild) tbody.removeChild(tbody.firstChild); }
var frag = document.createDocumentFragment();
rows.forEach(function (row) {
frag.appendChild(buildRow(row));
});
tbody.appendChild(frag);
}
function buildRow(row) {
var tr = mkEl('div', 'dsg-row');
var tdDSG = mkEl('div', 'dsg-cell dsg-cell-main col-dsg');
try {
tdDSG.innerHTML = (typeof App !== 'undefined' && App.createDSGRowHtml)
? App.createDSGRowHtml(row, 'dsg') : esc(row.drg);
} catch (e) { tdDSG.textContent = row.drg; }
if (row.diag_notes_matched && typeof App !== 'undefined' && App.notesSystem) {
var ageIconsHtml = '';
Object.keys(row.diag_notes_matched).forEach(function (label) {
ageIconsHtml += App.notesSystem.createAgeScopeIconsHtml(row.diag_notes_matched[label], true);
});
if (ageIconsHtml) {
var existingGroup = tdDSG.querySelector('.icons-group');
if (existingGroup) {
existingGroup.insertAdjacentHTML('afterbegin', ageIconsHtml);
} else {
tdDSG.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;"><span>' +
tdDSG.innerHTML + '</span><span class="icons-group">' + ageIconsHtml + '</span></div>';
}
}
}
var tdCoeff = mkEl('div', 'dsg-cell dsg-cell-center col-coeff');
tdCoeff.textContent = row.coefficient;
var extraHtml = row.skip_cost ? '' : (row.badges_html || '');
var tdExtra = mkEl('div', 'dsg-cell dod-coeff-cell col-extra');
tdExtra.innerHTML = extraHtml || '—';
if (typeof App !== 'undefined' && App.notesSystem) {
tdExtra.querySelectorAll('[data-icon-slot]').forEach(function (slot) {
slot.innerHTML = App.notesSystem.getIconUrl(slot.dataset.iconSlot);
});
}
var tdBaseRate = mkEl('div', 'dsg-cell dsg-cell-center col-base-rate');
tdBaseRate.dataset.cost = row.skip_cost ? '0' : String(row.base_rate_raw || 0);
tdBaseRate.textContent = row.base_rate || '—';
var tdCost = mkEl('div', 'dsg-cell dsg-cell-center col-cost');
tdCost.dataset.cost = row.skip_cost ? '0' : String(row.price_raw);
tdCost.textContent = row.price;
var tdBtn = mkEl('div', 'dsg-cell dsg-cell-btn col-actions');
var btnWrap = mkEl('div', 'btn-column');
var btnDiag = makeModalBtn('diagnosis', row, tr);
if (!row.diags_structured || !row.diags_structured.length) btnDiag.classList.add('hidden');
var btnSvc = makeModalBtn('service', row, tr);
if (!row.services_structured || !row.services_structured.length) btnSvc.classList.add('hidden');
btnWrap.appendChild(btnDiag);
btnWrap.appendChild(btnSvc);
tdBtn.appendChild(btnWrap);
tr.appendChild(tdDSG);
tr.appendChild(tdCoeff);
tr.appendChild(tdExtra);
tr.appendChild(tdBaseRate);
tr.appendChild(tdCost);
tr.appendChild(tdBtn);
return tr;
}
function makeModalBtn(type, row, tr) {
var isDiag = type === 'diagnosis';
var btn = mkEl('button', 'colored-icon-btn ' + (isDiag ? 'diagnosis' : 'service'));
btn.title = isDiag ? 'Діагнози' : 'Послуги';
btn.innerHTML = (isDiag
? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>')
+ '<span class="item-count">' + (isDiag ? row.diag_count : row.svc_count) + '</span>';
btn.addEventListener('click', function () {
if (typeof App === 'undefined' || !App.modalManager) return;
App.modalManager.setActiveRow(tr);
var filterValue = (isDiag ? (row.diag_search || '') : (row.svc_search || '')).replace(/ - /g, ' ');
var title = (isDiag ? 'Діагнози' : 'Послуги') + (row.drg ? ' | ' + row.drg : '');
if (isDiag) {
var scopeMap = row.diag_notes || {};
var items = (row.diags_structured || []).map(function (d) {
return scopeMap[d.code] ? Object.assign({}, d, { ageScope: scopeMap[d.code] }) : d;
});
showCodeNameModal(title, items, filterValue);
} else {
showCodeNameModal(title, row.services_structured || [], filterValue);
}
});
return btn;
}
function buildTableShell(cont) {
cont.innerHTML = '';
var table = mkEl('div', 'custom-table dsg-table-div');
var thead = mkEl('div', 'dsg-thead');
var hr = mkEl('div', 'dsg-header-row');
var cols = [
{ text: 'ДСГ', cls: 'col-dsg', sort: null },
{ text: 'Коефіцієнт', cls: 'col-coeff', sort: null },
{ text: 'Дод. коефіцієнти', cls: 'col-extra', sort: null },
];
cols.push(
{ text: 'Тариф, грн', cls: 'col-base-rate', sort: 'base_rate' },
{ text: 'Факт. оплата, грн', cls: 'col-cost', sort: 'cost' },
{ text: 'Переглянути', cls: 'col-actions', sort: null }
);
cols.forEach(function (col) {
var th = mkEl('div', 'dsg-th ' + col.cls);
if (col.sort) {
th.classList.add('sortable-header');
th.dataset.sort = col.sort; 
var span = document.createElement('span'); span.textContent = col.text;
var arrows = mkEl('span', 'sort-arrows');
['asc', 'desc'].forEach(function (dir) {
var a = mkEl('span', 'sort-arrow ' + dir);
a.title = dir === 'asc' ? 'За зростанням' : 'За спаданням';
if (PKG.sort === col.sort + '_' + dir) a.classList.add('active');
a.addEventListener('click', function (e) { e.stopPropagation(); applySort(col.sort + '_' + dir); });
arrows.appendChild(a);
});
th.appendChild(span); th.appendChild(arrows);
} else {
th.textContent = col.text;
}
hr.appendChild(th);
});
thead.appendChild(hr); table.appendChild(thead);
var tbody = mkEl('div', 'dsg-tbody');
table.appendChild(tbody);
cont.appendChild(table);
return tbody;
}
function buildSkeletonRows(tbody, count) {
var frag = document.createDocumentFragment();
for (var i = 0; i < count; i++) {
var tr = mkEl('div', 'dsg-row');
var tdDsg = mkEl('div', 'dsg-cell col-dsg');
tdDsg.appendChild(mkEl('div', 'cell-skeleton'));
tr.appendChild(tdDsg);
var tdCoeff = mkEl('div', 'dsg-cell col-coeff');
tdCoeff.appendChild(mkEl('div', 'cell-skeleton cell-skeleton-sm'));
tr.appendChild(tdCoeff);
var tdExtra = mkEl('div', 'dsg-cell col-extra');
tdExtra.appendChild(mkEl('div', 'cell-skeleton cell-skeleton-sm'));
tr.appendChild(tdExtra);
var tdBase = mkEl('div', 'dsg-cell col-base-rate');
tdBase.appendChild(mkEl('div', 'cell-skeleton cell-skeleton-sm'));
tr.appendChild(tdBase);
var tdCost = mkEl('div', 'dsg-cell col-cost');
tdCost.appendChild(mkEl('div', 'cell-skeleton cell-skeleton-sm'));
tr.appendChild(tdCost);
var tdBtn = mkEl('div', 'dsg-cell dsg-cell-btn col-actions');
var btnWrap = mkEl('div', 'btn-column');
btnWrap.appendChild(mkEl('div', 'btn-skeleton btn-skeleton-diagnosis'));
btnWrap.appendChild(mkEl('div', 'btn-skeleton btn-skeleton-service'));
tdBtn.appendChild(btnWrap);
tr.appendChild(tdBtn);
frag.appendChild(tr);
}
tbody.appendChild(frag);
}
function renderMeta(meta) {
var m1 = document.getElementById('metaInfo');
if (m1) { m1.innerHTML = 'Базова ставка: <strong>' + meta.RATE + '\u00A0грн</strong>'; m1.classList.add('show'); }
var m2 = document.getElementById('metaInfoAlt');
if (m2) { m2.innerHTML = 'Коеф. за пролікований випадок: <strong>' + meta.COEFF + '</strong>'; m2.classList.add('show'); }
}
function initCompactFilters() {
initDropdown('dsg', 'dropdown-dsg', 'dsg', true);
initDropdown('diagnosis', 'dropdown-diagnosis', 'diagnosis', false);
initDropdown('service', 'dropdown-service', 'service', false);
document.addEventListener('click', function (e) {
if (!e.target.closest('.filter-marker')) closeAllDropdowns();
});
}
function initDropdown(filterType, panelId, facetType, multiSelect) {
var marker = document.querySelector('[data-filter="' + filterType + '"]');
var panel = document.getElementById(panelId);
if (!marker || !panel) return;
var input = panel.querySelector('input[type="text"]');
var optList = panel.querySelector('.dropdown-options');
marker.addEventListener('click', function (e) {
e.stopPropagation();
if (e.target.closest('.filter-dropdown-panel')) return;
var wasOpen = panel.classList.contains('show');
closeAllDropdowns();
if (!wasOpen) {
panel.classList.add('show');
marker.classList.add('active');
requestAnimationFrame(function () { placeDropdown(marker, panel); });
if (input) { input.value = ''; input.focus(); }
loadSuggestions(_uiCtx, facetType, '', optList, filterType, multiSelect);
}
});
if (input) {
var t;
input.addEventListener('input', function () {
clearTimeout(t);
t = setTimeout(function () {
loadSuggestions(_uiCtx, facetType, input.value.trim(), optList, filterType, multiSelect);
}, 250);
});
}
optList.addEventListener('click', function (e) {
e.stopPropagation();
var opt = e.target.closest('.dropdown-option');
if (!opt) return;
var val = opt.dataset.value;
var partial = opt.dataset.partial === '1';
var key = partial ? '__partial__:' + val : val;
var label = partial ? '🗝️ ' + val : val;
if (multiSelect) {
if (CF[filterType].has(key)) CF[filterType].delete(key);
else CF[filterType].set(key, { text: label, partial: partial });
} else if (partial) {
var exactKeys = [];
CF[filterType].forEach(function (v, k) { if (!v.partial) exactKeys.push(k); });
exactKeys.forEach(function (k) { CF[filterType].delete(k); });
if (CF[filterType].has(key)) CF[filterType].delete(key);
else CF[filterType].set(key, { text: label, partial: true });
optList.querySelectorAll('.dropdown-option').forEach(function (o) {
var oKey = o.dataset.partial === '1' ? '__partial__:' + o.dataset.value : o.dataset.value;
var sel = CF[filterType].has(oKey);
o.classList.toggle('selected', sel);
var chk = o.querySelector('.option-checkbox');
if (chk) chk.classList.toggle('checked', sel);
});
if (input) { input.value = ''; input.focus(); }
loadSuggestions(_uiCtx, facetType, '', optList, filterType, multiSelect);
syncFilters(); updateChips();
debouncedReload();
return;
} else {
var wasSelected = CF[filterType].has(key);
CF[filterType].clear();
if (!wasSelected) CF[filterType].set(key, { text: label, partial: false });
closeAllDropdowns();
if (input) input.value = '';
syncFilters(); updateChips();
reloadNow();
return;
}
optList.querySelectorAll('.dropdown-option').forEach(function (o) {
var oKey = o.dataset.partial === '1' ? '__partial__:' + o.dataset.value : o.dataset.value;
var sel = CF[filterType].has(oKey);
o.classList.toggle('selected', sel);
var chk = o.querySelector('.option-checkbox');
if (chk) chk.classList.toggle('checked', sel);
});
syncFilters(); updateChips();
debouncedReload();
});
}
function initCoeffFilter() {
var marker = document.querySelector('.filter-marker-coefficients');
var dropdown = document.getElementById('dropdown-coefficients');
var infoBtn = document.getElementById('coeff-info-btn');
if (!marker || !dropdown) return;
if (infoBtn) {
infoBtn.addEventListener('click', function (e) {
e.stopPropagation();
if (typeof window.showCoeffDetails === 'function') window.showCoeffDetails();
});
}
marker.addEventListener('click', function (e) {
e.stopPropagation();
if (e.target.closest('#coeff-info-btn')) return;
var wasOpen = dropdown.classList.contains('show');
closeAllDropdowns();
if (!wasOpen) {
dropdown.classList.add('show');
marker.classList.add('active');
requestAnimationFrame(function () { placeDropdown(marker, dropdown); });
}
});
dropdown.querySelectorAll('.coeff-option').forEach(function (option) {
option.addEventListener('click', function (e) {
e.stopPropagation();
var cb = option.querySelector('input[type="checkbox"]');
var val = parseFloat(cb.value);
cb.checked = !cb.checked;
if (cb.checked) CF.coeffs.add(val); else CF.coeffs.delete(val);
syncFilters(); updateChips(); debouncedReload();
});
});
}
function syncFilters() {
function split(map) {
var ex = [], pa = [];
map.forEach(function (v, k) {
if (v.partial) pa.push(k.replace('__partial__:', ''));
else ex.push(k);
});
return { ex: ex, pa: pa };
}
var d = split(CF.dsg), g = split(CF.diagnosis), s = split(CF.service);
PKG.filters.dsg_ex = d.ex; PKG.filters.dsg_pa = d.pa;
PKG.filters.diag_ex = g.ex; PKG.filters.diag_pa = g.pa;
PKG.filters.svc_ex = s.ex; PKG.filters.svc_pa = s.pa;
PKG.filters.coeffs = Array.from(CF.coeffs);
invalidateFacetsCache();
}
var CHIP_CLS = { dsg: 'type-dsg', diagnosis: 'type-diagnosis', service: 'type-service' };
function displayCoeff(v) {
var display = { 1.22: '1.2', 1.21: '1.2', 0.6: '0.6', 0.8: '0.8', 1.1: '1.1', 1.3: '1.3', 2.1: 'Діти', 2.2: 'Травми' };
return display[v] !== undefined ? String(display[v]) : String(v);
}
function coeffChipCls(v) {
var m = { 1.22:'type-coefficient-22', 1.21:'type-coefficient-21', 1.3:'type-coefficient-13', 0.8:'type-coefficient-08', 1.1:'type-coefficient-11', 2.1:'type-coefficient-children', 2.2:'type-coefficient-trauma' };
return m[v] || 'type-coefficient';
}
function updateChips() {
var cont = document.getElementById('chips-container');
var countEl = document.getElementById('chips-count');
var clearBtn = document.getElementById('clear-all');
if (!cont) return;
cont.innerHTML = '';
var n = 0;
function chip(label, cls, fn) {
n++;
var c = mkEl('div', 'filter-chip ' + cls);
var s = mkEl('span'); s.textContent = label;
var b = mkEl('button', 'chip-remove'); b.textContent = '×';
b.addEventListener('click', fn);
c.appendChild(s); c.appendChild(b);
cont.appendChild(c);
}
CF.dsg.forEach(function (v, k) { chip(v.text, CHIP_CLS.dsg, function () { CF.dsg.delete(k); syncFilters(); updateChips(); reloadNow(); }); });
CF.diagnosis.forEach(function (v, k) { chip(v.text, CHIP_CLS.diagnosis, function () { CF.diagnosis.delete(k); syncFilters(); updateChips(); reloadNow(); }); });
CF.service.forEach(function (v, k) { chip(v.text, CHIP_CLS.service, function () { CF.service.delete(k); syncFilters(); updateChips(); reloadNow(); }); });
CF.coeffs.forEach(function (val) {
chip('Коеф.\u00A0' + displayCoeff(val), coeffChipCls(val), function () {
CF.coeffs.delete(val);
var cb = document.querySelector('.coeff-option input[value="' + val + '"]');
if (cb) cb.checked = false;
syncFilters(); updateChips(); reloadNow();
});
});
if (countEl) countEl.textContent = n;
if (clearBtn) clearBtn.style.display = n > 0 ? '' : 'none';
App.updateSearchWarning();
[['dsg', CF.dsg], ['diagnosis', CF.diagnosis], ['service', CF.service]].forEach(function (p) {
var mk = document.querySelector('[data-filter="' + p[0] + '"]');
if (!mk) return;
var b = mk.querySelector('.marker-badge');
if (b) { b.textContent = p[1].size; b.style.display = p[1].size > 0 ? '' : 'none'; }
mk.classList.toggle('has-filter', p[1].size > 0);
});
var cm = document.querySelector('.filter-marker-coefficients');
if (cm) {
var b = cm.querySelector('.marker-badge');
if (b) { b.textContent = CF.coeffs.size; b.style.display = CF.coeffs.size > 0 ? '' : 'none'; }
cm.classList.toggle('has-filter', CF.coeffs.size > 0);
}
}
function initClearAll() {
var btn = document.getElementById('clear-all');
if (!btn) return;
btn.addEventListener('click', function () {
CF.dsg.clear(); CF.diagnosis.clear(); CF.service.clear(); CF.coeffs.clear();
document.querySelectorAll('.coeff-option input[type="checkbox"]').forEach(function (cb) { cb.checked = false; });
syncFilters(); updateChips(); reloadNow();
});
}
function reloadNow() { loadRows(false); }
var debouncedReload = App.debounce(reloadNow, 280);
function applySort(s) {
PKG.sort = PKG.sort === s ? '' : s;
document.querySelectorAll('.sort-arrow').forEach(function (a) {
var col = a.closest('.sortable-header');
if (!col) return;
var colSort = col.dataset.sort || '';
var isAsc = a.classList.contains('asc');
var isDesc = a.classList.contains('desc');
a.classList.toggle('active',
(isAsc && PKG.sort === colSort + '_asc') ||
(isDesc && PKG.sort === colSort + '_desc')
);
});
reloadNow();
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