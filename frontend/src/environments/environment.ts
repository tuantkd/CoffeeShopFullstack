export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffee-shop.uk', // the auth0 domain prefix
    audience: 'coffeeshop', // the audience set for the auth0 app
    clientId: '5XpxbTBYQDOcUCN9SAc6PCbAwFMrjyNa', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
