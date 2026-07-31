## Overview

URL Shorteners shorten extremely long urls, into much shorter URLs
However, millions of URLs needed to be shortened every day, approximately 100 million per day, which over 10 years means storing 365 billion URLs.

Including a - z, A - Z, 0 - 9, we get 62 characters, so to cover that 365 billion mark easily, we’d make 7 letter long URLs since 62^7
is close to 3.5 trillion.

```Long Variable Length URL --> 7 bit string URL```

Two main actions are performed in a URL Shortener:
- Shortening the link itself
- Redirect process after a shortened URL is clicked

## Methods to Shorten a URL

Hashing isn’t a viable method mainly because even the smallest hashing functions lead to 32 bit hashes which is too large for the requirement at hand, which is 7.

Counting is mainly implemented, where the next time a person wants to shorten a URL, the next string sequence is used, which means no collisions like in hashing and no need to perform database lookups.
Only issues with counting are the security risk of an attacker guessing and scaling issue where we need to maintain unique URLs across many servers.

## On Link Click

Clicking short links happens more often than creating new short links, so speed is required.  On clicking a short URL

```
Check Cache --> Check Database --> Cache Result --> Redirect to Original URL
```

Usually during the redirect a **301** HTTP status code is used to tell the browser that the resource has permanently moved to the longer URL, so next time the browser automatically knows.

Article: [How a URL Shortener Works in Real Systesm](https://medium.com/@rajatraghav7797/everyone-draws-a-url-shortener-few-explain-how-it-actually-generates-unique-ids-08b34199b1f6)
