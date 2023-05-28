#!/usr/bin/env node

const cdk = require('aws-cdk-lib');
const { PlaywrightLambdaStack } = require('../lib/cdk-stack');

const app = new cdk.App();
new PlaywrightLambdaStack(app, 'PlaywrightLambdaStack', {
    env: { region: 'ap-northeast-2' },
});
