const ENV = process.env.ENV || 'dev';

const config = {
  dev: 'https://public-api-gateway.carstensz.privydev.id',
  stag: 'https://stg-public-api.privy.id',
  prod: 'https://api-carstensz.privy.id'
};

module.exports = config[ENV];
