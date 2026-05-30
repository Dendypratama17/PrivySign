const request = require('supertest');
const BASE_URL = require('../config/env');
const { getAuthHeader } = require('../config/auth');

const api = request(BASE_URL);
const { randomUUID } = require('crypto');

const headers = {
  Authorization: getAuthHeader(),
  'Content-Type': 'application/json',
  'X-Application-Name': 'PrivySign',
  'X-Platform-Name': 'API',
  'X-Platform-Type': 'Automation API',
  'X-Request-ID': randomUUID(),
  'X-Application-Version': '0.0.0.1',
};

module.exports = { api, headers };

describe('Contacts API Automation', () => {

  // =========================
  // TC-API-01
  // =========================
  test('TC-API-01 Import single valid registered number', async () => {

    const createRes = await api
      .post('/privysign/v1/users/contacts')
      .set(headers)
      .send({
        contacts: [
            { phone_number: '+628513103085' }
        ]});

    // const createdPrivyId = createRes.body.data.success[0].privy_id;

    // console.log('POST privy_id:', createdPrivyId);
    console.log(JSON.stringify(createRes.body, null, 2));
    // expect(createRes.statusCode).toBe(201);
    // expect(createRes.body.message).toContain('successfully_save_contact');

    const getRes = await api
      .get('/privysign/v1/users/contacts/list')
      .set(headers);


    // const getPrivyIds = getRes.body.data.map(c => c.privy_id);

    // console.log('GET privy_ids:', getPrivyIds);
    console.log(getRes.body);
    // expect(getPrivyIds.includes(createdPrivyId)).toBe(true);
    // expect(getRes.statusCode).toBe(200);
    // expect(getRes.body.message).toContain('successfully_list_contact');


    const extractContactIds = (res) => { return res.body?.data?.map(c => c.id) || []; };
    const contactIds = extractContactIds(getRes);
    console.log('Contact_ID:', contactIds);

    // for (const id of contactIds) {
    //   const deleteRes = await api
    //     .delete(`/privysign/v1/users/contacts/${id}`)
    //     .set(headers);

    //   console.log('DELETE RESPONSE:', deleteRes.body);

    //   expect(deleteRes.statusCode).toBe(200);
    //   expect(deleteRes.body.message).toContain('successfully_delete_contact');
    // }
  });

  // =========================
  // TC-API-02
  // =========================
  // test('TC-API-02 Import multiple registered numbers', async () => {

  //   const createRes = await api
  //     .post('/privysign/v1/users/contacts')
  //     .set(headers)
  //     .send({
  //     contacts: [
  //       { phone_number: '+628513103085' },
  //       { phone_number: '089507747573' }
  //     ]
  //   });

  //   const createdPrivyId = createRes.body.data.success[0].privy_id;

  //   console.log('POST privy_id:', createdPrivyId);
  //   console.log(JSON.stringify(createRes.body, null, 2));
  //   expect(createRes.statusCode).toBe(201);
  //   expect(createRes.body.message).toContain('successfully_save_contact');

  //   const getRes = await api
  //     .get('/privysign/v1/users/contacts/list')
  //     .set(headers);


  //   const getPrivyIds = getRes.body.data.map(c => c.privy_id);

  //   console.log('GET privy_ids:', getPrivyIds);
  //   console.log(getRes.body);
  //   expect(getPrivyIds.includes(createdPrivyId)).toBe(true);
  //   expect(getRes.statusCode).toBe(200);
  //   expect(getRes.body.message).toContain('successfully_list_contact');


  //   const extractContactIds = (res) => { return res.body?.data?.map(c => c.id) || []; };
  //   const contactIds = extractContactIds(getRes);
  //   console.log('Contact_ID:', contactIds);

  //   for (const id of contactIds) {
  //     const deleteRes = await api
  //       .delete(`/privysign/v1/users/contacts/${id}`)
  //       .set(headers);

  //     console.log('DELETE RESPONSE:', deleteRes.body);

  //     expect(deleteRes.statusCode).toBe(200);
  //     expect(deleteRes.body.message).toContain('successfully_delete_contact');
  //   }
  // });

  // // =========================
  // // TC-API-03
  // // =========================
  // test('TC-API-03 Mixed registered & unregistered', async () => {

  //   const createRes = await api
  //     .post('/privysign/v1/users/contacts')
  //     .set(headers)
  //     .send({
  //     contacts: [
  //       { phone_number: '+628513103085' },
  //       { phone_number: '62900000711' }
  //     ]
  //   });

  //   const createdPrivyId = createRes.body.data.success[0].privy_id;

  //   console.log('POST privy_id:', createdPrivyId);
  //   console.log(JSON.stringify(createRes.body, null, 2));
  //   expect(createRes.statusCode).toBe(201);
  //   expect(createRes.body.message).toContain('successfully_save_contact');

  //   const getRes = await api
  //     .get('/privysign/v1/users/contacts/list')
  //     .set(headers);


  //   const getPrivyIds = getRes.body.data.map(c => c.privy_id);

  //   console.log('GET privy_ids:', getPrivyIds);
  //   console.log(getRes.body);
  //   expect(getPrivyIds.includes(createdPrivyId)).toBe(true);
  //   expect(getRes.statusCode).toBe(200);
  //   expect(getRes.body.message).toContain('successfully_list_contact');

  // /*  
  //   const extractContactIds = (res) => { return res.body?.data?.map(c => c.id) || []; };
  //   const contactIds = extractContactIds(getRes);
  //   console.log('Contact_ID:', contactIds);

  //   for (const id of contactIds) {
  //     const deleteRes = await api
  //       .delete(`/privysign/v1/users/contacts/${id}`)
  //       .set(headers);

  //     console.log('DELETE RESPONSE:', deleteRes.body);

  //     expect(deleteRes.statusCode).toBe(200);
  //     expect(deleteRes.body.message).toContain('successfully_delete_contact');
  //   // }
  // */
  // });

  // // =========================
  // // TC-API-04
  // // =========================
  // test('TC-API-04 Duplicate phone numbers', async () => {

  //    const createRes = await api
  //     .post('/privysign/v1/users/contacts')
  //     .set(headers)
  //     .send({
  //     contacts: [
  //       { phone_number: '+628513103085' },
  //       { phone_number: '089507747573' }
  //     ]
  //   });

  //   const createdPrivyId = createRes.body.data.success[0].privy_id;

  //   console.log('POST privy_id:', createdPrivyId);
  //   console.log(JSON.stringify(createRes.body, null, 2));
  //   expect(createRes.statusCode).toBe(201);
  //   expect(createRes.body.message).toContain('successfully_save_contact');

  //   const getRes = await api
  //     .get('/privysign/v1/users/contacts/list')
  //     .set(headers);

  //   const getPrivyIds = getRes.body.data.map(c => c.privy_id);

  //   console.log('GET privy_ids:', getPrivyIds);
  //   console.log(getRes.body);
  //   expect(getPrivyIds.includes(createdPrivyId)).toBe(true);
  //   expect(getRes.statusCode).toBe(200);
  //   expect(getRes.body.message).toContain('successfully_list_contact');


  //   const extractContactIds = (res) => { return res.body?.data?.map(c => c.id) || []; };
  //   const contactIds = extractContactIds(getRes);
  //   console.log('Contact_ID:', contactIds);

  //   for (const id of contactIds) {
  //     const deleteRes = await api
  //       .delete(`/privysign/v1/users/contacts/${id}`)
  //       .set(headers);

  //     console.log('DELETE RESPONSE:', deleteRes.body);

  //     expect(deleteRes.statusCode).toBe(200);
  //     expect(deleteRes.body.message).toContain('successfully_delete_contact');
  //   }
  // });

  // // =========================
  // // TC-API-05
  // // =========================
  // test('TC-API-05 Invalid phone number format', async () => {


  //   const phoneNumber = '12345abcde'
  //   const last2 = phoneNumber.slice(-2);
  //   const createRes = await api
  //     .post('/privysign/v1/users/contacts')
  //     .set(headers)
  //     .send({
  //     contacts: [
  //       { phone_number: (phoneNumber) }
  //     ]
  //   });

  //   console.log(JSON.stringify(createRes.body, null, 2));
  //   expect(createRes.statusCode).toBe(422);
  //   expect(createRes.body.message).toContain('Unprocessable Entity');

  //   const getRes = await api
  //     .get('/privysign/v1/users/contacts/list')
  //     .set(headers);

  //   console.log(getRes.body);
  //   expect(getRes.statusCode).toBe(200);
  //   expect(getRes.body.message).toContain('successfully_list_contact');
  //   expect(getRes.body.data.some(c => c.phone === last2)).toBe(false);
  // });
  
});