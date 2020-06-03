import React from 'react';
import md5 from 'crypto-js/md5';

const finderSpan = (finder, possessive = false, ownItem = false) => (
  <span className={ `finder-span ${ownItem ? 'mine' : null}` }>{finder}{possessive ? "'s" : null}</span>
);
const recipientSpan = (recipient, possessive = false, ownItem = false) => (
  <span className={ `recipient-span ${ownItem ? 'mine' : null}` }>{recipient}{possessive ? "'s" : null}</span>
);
const itemSpan = (item) => <span className="item-span">{item}</span>;
const locationSpan = (location) => <span className="location-span">{location}</span>;
const entranceSpan = (entrance) => <span className="entrance-span">{entrance}</span>;

class MonitorTools {
  /** Convert plaintext into a React-friendly div */
  static createTextDiv = (text) => (
    <div key={ `${md5(text)}${Math.floor((Math.random() * 1000000))}` }>
      {text}
    </div>
  );

  /** Sent an item to another player */
  static sentItem = (finder, recipient, item, location, iAmFinder = false, iAmRecipient = false) => (
    <div
      key={ `${md5(finder + recipient + item + location)}${Math.floor((Math.random() * 1000000))}` }
      className={ (iAmFinder || iAmRecipient) ? 'relevant' : null }
    >
      {finderSpan(finder, false, iAmFinder)} found {recipientSpan(recipient, true, iAmRecipient)}&nbsp;
      {itemSpan(item)} at {locationSpan(location)}
    </div>
  )

  /** Received item from another player */
  static receivedItem = (finder, item, location, itemIndex, queueLength) => (
    <div
      key={ `${md5(finder + item + location)}${Math.floor((Math.random() * 1000000))}` }
      className="relevant"
    >
      ({itemIndex}/{queueLength}) {finderSpan(finder, false)} found your&nbsp;
      {itemSpan(item)} at {locationSpan(location)}
    </div>
  )

  /** Player found their own item (local or remote player) */
  static foundItem = (finder, item, location, iAmFinder = false) => (
    <div
      key={ `${md5(finder + item + location)}${Math.floor((Math.random() * 1000000))}` }
      className={ iAmFinder ? 'relevant' : null }
    >
      {finderSpan(finder, false, iAmFinder)} found their own {itemSpan(item)} at {locationSpan(location)}
    </div>
  )

  /** Hint message */
  static hintMessage = (finder, recipient, item, location, found, iAmFinder = false, iAmRecipient = false,
    entranceLocation = null) => (
      <div
        key={ `${md5(finder + recipient + item + location)}${Math.floor((Math.random() * 1000000))}` }
        className={ (iAmFinder || iAmRecipient) ? 'relevant' : null }
      >
        {recipientSpan(recipient, true, iAmRecipient)} {itemSpan(item)} can be found in&nbsp;
        {finderSpan(finder, true, iAmFinder)} world at {locationSpan(location)}
        { entranceLocation ? [', which is at ', entranceSpan(entranceLocation)] : null }&nbsp;
        ({found ? '✔' : '❌'})
      </div>
  )
}

export default MonitorTools;
