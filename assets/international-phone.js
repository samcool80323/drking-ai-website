(() => {
  'use strict';

  const CALLING_CODES = {
    AC:'247',AD:'376',AE:'971',AF:'93',AG:'1',AI:'1',AL:'355',AM:'374',AO:'244',AR:'54',AS:'1',AT:'43',AU:'61',AW:'297',AX:'358',AZ:'994',BA:'387',BB:'1',BD:'880',BE:'32',BF:'226',BG:'359',BH:'973',BI:'257',BJ:'229',BL:'590',BM:'1',BN:'673',BO:'591',BQ:'599',BR:'55',BS:'1',BT:'975',BW:'267',BY:'375',BZ:'501',CA:'1',CC:'61',CD:'243',CF:'236',CG:'242',CH:'41',CI:'225',CK:'682',CL:'56',CM:'237',CN:'86',CO:'57',CR:'506',CU:'53',CV:'238',CW:'599',CX:'61',CY:'357',CZ:'420',DE:'49',DJ:'253',DK:'45',DM:'1',DO:'1',DZ:'213',EC:'593',EE:'372',EG:'20',EH:'212',ER:'291',ES:'34',ET:'251',FI:'358',FJ:'679',FK:'500',FM:'691',FO:'298',FR:'33',GA:'241',GB:'44',GD:'1',GE:'995',GF:'594',GG:'44',GH:'233',GI:'350',GL:'299',GM:'220',GN:'224',GP:'590',GQ:'240',GR:'30',GT:'502',GU:'1',GW:'245',GY:'592',HK:'852',HN:'504',HR:'385',HT:'509',HU:'36',ID:'62',IE:'353',IL:'972',IM:'44',IN:'91',IO:'246',IQ:'964',IR:'98',IS:'354',IT:'39',JE:'44',JM:'1',JO:'962',JP:'81',KE:'254',KG:'996',KH:'855',KI:'686',KM:'269',KN:'1',KP:'850',KR:'82',KW:'965',KY:'1',KZ:'7',LA:'856',LB:'961',LC:'1',LI:'423',LK:'94',LR:'231',LS:'266',LT:'370',LU:'352',LV:'371',LY:'218',MA:'212',MC:'377',MD:'373',ME:'382',MF:'590',MG:'261',MH:'692',MK:'389',ML:'223',MM:'95',MN:'976',MO:'853',MP:'1',MQ:'596',MR:'222',MS:'1',MT:'356',MU:'230',MV:'960',MW:'265',MX:'52',MY:'60',MZ:'258',NA:'264',NC:'687',NE:'227',NF:'672',NG:'234',NI:'505',NL:'31',NO:'47',NP:'977',NR:'674',NU:'683',NZ:'64',OM:'968',PA:'507',PE:'51',PF:'689',PG:'675',PH:'63',PK:'92',PL:'48',PM:'508',PR:'1',PS:'970',PT:'351',PW:'680',PY:'595',QA:'974',RE:'262',RO:'40',RS:'381',RU:'7',RW:'250',SA:'966',SB:'677',SC:'248',SD:'249',SE:'46',SG:'65',SH:'290',SI:'386',SJ:'47',SK:'421',SL:'232',SM:'378',SN:'221',SO:'252',SR:'597',SS:'211',ST:'239',SV:'503',SX:'1',SY:'963',SZ:'268',TA:'290',TC:'1',TD:'235',TG:'228',TH:'66',TJ:'992',TK:'690',TL:'670',TM:'993',TN:'216',TO:'676',TR:'90',TT:'1',TV:'688',TW:'886',TZ:'255',UA:'380',UG:'256',US:'1',UY:'598',UZ:'998',VA:'39',VC:'1',VE:'58',VG:'1',VI:'1',VN:'84',VU:'678',WF:'681',WS:'685',XK:'383',YE:'967',YT:'262',ZA:'27',ZM:'260',ZW:'263'
  };
  const COMMON_COUNTRIES = ['AU', 'NZ', 'GB', 'US', 'CA', 'IN', 'SG', 'AE'];
  const SIGNIFICANT_LEADING_ZERO = new Set(['CI', 'IT', 'MO', 'SM', 'SJ', 'SZ', 'VA']);
  const displayNames = typeof Intl.DisplayNames === 'function'
    ? new Intl.DisplayNames([document.documentElement.lang || 'en-AU'], { type: 'region' })
    : null;

  const countryName = (code) => {
    try { return displayNames?.of(code) || code; } catch { return code; }
  };
  const flag = (code) => code.replace(/[A-Z]/g, (letter) => String.fromCodePoint(127397 + letter.charCodeAt()));
  const countryOrder = Object.keys(CALLING_CODES).sort((a, b) => {
    const commonA = COMMON_COUNTRIES.indexOf(a);
    const commonB = COMMON_COUNTRIES.indexOf(b);
    if (commonA !== -1 || commonB !== -1) return (commonA === -1 ? 99 : commonA) - (commonB === -1 ? 99 : commonB);
    return countryName(a).localeCompare(countryName(b));
  });

  const detectedLocaleCountry = () => {
    const locale = navigator.languages?.[0] || navigator.language || '';
    const code = locale.match(/[-_]([A-Z]{2})\b/i)?.[1]?.toUpperCase();
    return code && CALLING_CODES[code] ? code : 'AU';
  };

  const normalisePhone = (value, country) => {
    const trimmed = String(value || '').trim();
    const international = trimmed.startsWith('+') || trimmed.startsWith('00');
    const digits = trimmed.replace(/\D/g, '');
    if (!digits) return '';
    if (international) return `+${trimmed.startsWith('00') ? digits.slice(2) : digits}`;
    const nationalNumber = SIGNIFICANT_LEADING_ZERO.has(country) ? digits : digits.replace(/^0+/, '');
    return `+${CALLING_CODES[country] || CALLING_CODES.AU}${nationalNumber}`;
  };

  const validate = (input) => {
    const select = input.closest('[data-international-phone]')?.querySelector('select');
    const value = normalisePhone(input.value, select?.value || 'AU');
    input.dataset.e164 = value;
    input.setCustomValidity(!value || !/^\+[1-9]\d{6,14}$/.test(value)
      ? 'Enter a valid phone number, including the area code.'
      : '');
    return value;
  };

  const selectCountry = (select, code) => {
    if (!CALLING_CODES[code]) return;
    select.value = code;
    const input = select.closest('[data-international-phone]')?.querySelector('input[type="tel"]');
    if (input) {
      input.placeholder = code === 'AU' ? '0412 345 678' : 'Phone number';
      validate(input);
    }
  };

  const controls = [...document.querySelectorAll('input[type="tel"]')].map((input) => {
    if (input.closest('[data-international-phone]')) return input.closest('[data-international-phone]');
    input.required = true;
    input.autocomplete = 'tel-national';
    input.inputMode = 'tel';
    input.setAttribute('aria-describedby', [input.getAttribute('aria-describedby'), `${input.id}-phone-help`].filter(Boolean).join(' '));

    const control = document.createElement('div');
    control.className = 'international-phone-control';
    control.dataset.internationalPhone = '';
    const select = document.createElement('select');
    select.className = 'country-code-select';
    select.setAttribute('aria-label', 'Country calling code');
    select.name = `${input.name || 'phone'}Country`;
    for (const code of countryOrder) {
      const option = document.createElement('option');
      option.value = code;
      option.textContent = `${flag(code)} +${CALLING_CODES[code]} ${countryName(code)}`;
      select.append(option);
    }
    input.before(control);
    control.append(select, input);
    const help = document.createElement('small');
    help.id = `${input.id}-phone-help`;
    help.className = 'phone-help';
    help.textContent = 'Country code is selected automatically. You can change it.';
    control.after(help);
    selectCountry(select, detectedLocaleCountry());
    select.addEventListener('change', () => selectCountry(select, select.value));
    input.addEventListener('input', () => validate(input));
    input.addEventListener('blur', () => validate(input));
    return control;
  });

  document.addEventListener('submit', (event) => {
    const form = event.target.closest?.('form[data-drking-form]');
    if (!form) return;
    form.querySelectorAll('input[type="tel"]').forEach(validate);
  }, true);

  if (controls.length) {
    fetch('/api/country', { headers: { Accept: 'application/json' }, cache: 'no-store' })
      .then((response) => response.ok ? response.json() : null)
      .then((result) => {
        const code = String(result?.country || '').toUpperCase();
        if (!CALLING_CODES[code]) return;
        controls.forEach((control) => selectCountry(control.querySelector('select'), code));
      })
      .catch(() => {});
  }

  window.DrKingPhone = { normalisePhone, validate };
})();
