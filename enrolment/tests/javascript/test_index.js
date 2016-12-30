var jsdom = require('jsdom').jsdom;
var expect = require('chai').expect;
var sinon = require('sinon');

var html = '\
<!doctype html> \
<html> \
  <body> \
    <div> \
      <a class="js-track-mailto-click" href="mailto:test@example.com">email me</a> \
    </div> \
  </body> \
</html> \
';

function requireUncached(module){
    delete require.cache[require.resolve(module)]
    return require(module)
}

describe('mailto click tracking', function() {

  beforeEach(function() {
    global.document = jsdom(html);
    global.ga = sinon.spy();
    requireUncached('../../static/javascripts/index.js');
  });

  it('should show the menu if currently hidden', function() {

    // when I click the email button
    var emailButton = document.querySelectorAll('.js-track-mailto-click')[0];
    emailButton.click();
    // then the google analytics track event fires
    sinon.assert.calledWith(global.ga,
      'send',
      'event',
      {
        eventCategory: 'Mailto link',
        eventAction: 'click',
        eventLabel: 'mailto:test@example.com',
      }
    );
  });

});