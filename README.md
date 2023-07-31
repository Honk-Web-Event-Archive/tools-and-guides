Requirements:
- Python
- XAMMP / Apache
- Fiddler
- Any IDE with RegEx search support
- Honkai Impact 3
- Any browser

Open Fiddler and open up the web event in-game. you can grab the event URL using Fiddler. It should look something like `https://act.hoyoverse.com/bh3/event/e20230626preheating-cc1dq5/...` Then, right click, "Copy URL", and open it in a browser.

Disable JS. If you have the uBlock extension installed , they have a toggle for disabling JS on a site.

Then download the site. Save it as `index.html`. A folder will be generated containing the files it accesses called `index_files`

If you are using XAMMP, place `index.html` and the `index_files` folder in a subfolder under `C:\xampp\htdocs`. You can name that subfolder anything but I will name it the same name as the original (e.g. `e20230724music`). 

Rename the .js files from `*.js.download` to `*.js`. There will be files like `main.js(1).download`. You can rename it to `main.1.js`. Don't forget to rename them in your `index.html` as well.

Move the `styles_...css` file up one folder, so that it is in the same path as `index.html`, and then change its href accordingly. Our CSS needs to access files relative to the current page. You could also just use relative paths that go up one level in your CSS. Pick your poison.
```html
<link href="./styles_cdbbac6bc87507f78368.css" rel="stylesheet" />
```

Copy all files in this repo's `tools` folder to your project's folder. To be clear, `.htaccess` should be in the same folder as `index.html`

Rename `index.html` to `index.php`. Place this at the top. There's some code that absolutely needs that parameter filled or else it won't load.
```php
<?php
if (!isset($_GET['authkey'])) {    
    $url = $_SERVER['REQUEST_URI'];
    if (strpos($url, '?') !== false) {
        $url .= '&authkey=ignore_this';
    } else {
        $url .= '?authkey=ignore_this';
    }
    header('Location: ' . $url);
    exit;
}
?>
```

Format all the .js files. I use [Prettier](https://www.npmjs.com/package/prettier).

Search for the pattern `#.p + "url"` (regex: `(?<=\w\.p \+ ").+(?=")`)

paste those strings in `asset_downloader.py`. It will download those files while also creating their respective folders.

Next, it'll by default set the user's language to Chinese. To fix this, search for this  
(regex: `\(\w\.IS_SEA \= \w\w\),`):
```js
(e.IS_CGHK4E = qt),
(e.IS_GAME = nn),
(e.IS_IOS = Yt),
(e.IS_MOB = Wt),
(e.IS_PS = $t),
(e.IS_RUN_CGHK4E = Jt),
(e.IS_SEA = on),
(e.IS_WECHAT = Zt),
(e.LANG_MAP = dt),
```

Scroll up until you find the number that refers to that function.

```js
9134: function (e, t, n) {
```

Search for it being assigned to a var (regex: `\w \= \w\(9134\)`):
```js
P = r(9134),
```

Scroll down the list of variable assignments and set that variable's `IS_SEA` to true. It's a little dirty but it works:
```js
P = r(9134),
...
...
it = r.n(nt),
ot = r(50618),
at = r.n(ot),
ct = r(54698),
ut = r.n(ct);
P.IS_SEA = true;
```

It will fail to load `'./admin/mi18n/bh3_global/.../...-en-us.json'` in the console. Open that url in a browser, and download it. Put it in your project folder, and keep the folder structure (you can use `make_dirs.py`) so the site is still able to access it.

Then, we need to redirect the site's requests from their servers to ours.

Search for `BASE_HOST_LIST`. You'll find something like this. Remove the hoyoverse part. (No leading slash. It shows up in many different places. Be sure to check them all)
```js
s3: {
  inner: {
    prd: "admin/mi18n",
    sea: "admin/mi18n",
    pre: "https://webstatic-pre.hoyoverse.com/admin/mi18n",
    presea: "https://webstatic-pre.hoyoverse.com/admin/mi18n",
    test: "https://webstatic-test.hoyoverse.com/admin/mi18n",
    testsea:
      "https://webstatic-test.hoyoverse.com/admin/mi18n",
  },
  default: {
    prd: "admin/mi18n",
    sea: "admin/mi18n",
    pre: "https://webstatic-pre.hoyoverse.com/admin/mi18n",
    presea: "https://webstatic-pre.hoyoverse.com/admin/mi18n",
    test: "https://webstatic-test.hoyoverse.com/admin/mi18n",
    testsea:
      "https://webstatic-test.hoyoverse.com/admin/mi18n",
  },
```

You can search `https://webstatic.hoyoverse.com/` and you'll find something like this. Set it to blank.
```js
          ot = {
            development: "https://webstatic-test.hoyoverse.com",
            test: "https://webstatic-test.hoyoverse.com",
            prerelease: "https://webstatic-pre.hoyoverse.com",
            production: "",
          },
```

There will be another JSON file. Do the same. Download it, then maintain the folder structure. 

`device-fp/api/getExtList` will fail to fetch. This time, just copy the contents. Copy the folder structure, and make a `getExtList.php` in that folder. Paste this in, with your JSON inside the `echo` statement.

```php
<?php
header('Content-Type: application/json');
echo 'PASTE YOUR JSON CONTENTS HERE';
?>
```

Look for this and remove the leading slashes. We don't want to fetch at the root of our url.
```js
(e.APIS = {
    getFp: "device-fp/api/getFp",
    getExtList: "device-fp/api/getExtList",
}),
```

Create a `getFp.php` file in the same folder as `getExtList.php` and do the same thing. You can't view the contents directly in the official URL cuz it only accepts POST requests, so view it in the network tab.

Next, is the authentication key. Similar thing with `getExtList.php` and `getFp.php`. To redirect it, find and rename `sg-public-data-api.hoyoverse.com` to a blank in the files. It showed up at least four times for me. I found them in `main.2.js`.  
`getFp` and `getExtList` also use this URL so that's three birds with one stone.
```js
(e.API_BASE = "https://sg-public-api.hoyoverse.com"),
```

They were a bit sneaky and separated the URL. Look for `sg-public-api` and set it to blank.
```js
        (t.apiPre = {
          test: "testing-sg-public-api",
          prerelease: "pre-sg-public-api",
          production: "sg-public-api",
        });
```

Look for this and set the `production` value to `common/badge/v1`

```js
        (e.API_BASE_SEA = {
          development:
            "https://testing-sg-public-api.{host}.com/common/badge/v1",
          test: "https://testing-sg-public-api.{host}.com/common/badge/v1",
          prerelease: "https://pre-sg-public-api.{host}.com/common/badge/v1",
          production: "https://sg-public-api.{host}.com/common/badge/v1",
        }),
```

`/admin/mi18n/plat_oversea/.../...json` will fail in the console. Search for `e.MI18N_BASE_SEA` and replace it with `admin/mi18n/` (no leading slash)
```js
        (e.MI18N_BASE_SEA = {
          development: "https://webstatic-test.hoyoverse.com/admin/mi18n/",
          test: "https://webstatic-test.hoyoverse.com/admin/mi18n/",
          prerelease: "https://webstatic-pre.hoyoverse.com/admin/mi18n/",
          production: "https://webstatic.hoyoverse.com/admin/mi18n/",
        }),
```

Go to that json on the original site and copy it over to the right folder, just like the previous ones. 

`'https://sg-public-api.hoyoverse.com/event/.../index` will fail.   
Look for this and change it to just `event/e20230724concert`. 

```js
        It = r
          .n(vt)()
          .create({
            baseURL:
              "https://sg-public-api.hoyoverse.com/event/e20230724concert",
            withCredentials: !0,
          });
```

Then copy the directories, and make an `index.php` file there. Since this is event progress data, you probably want to view and edit the contents of that response. You can create an `index.json` file in the same folder, and then read and send it back using this:

```php
<?php
header('Content-Type: application/json');
echo file_get_contents("index.json");
?>
```

We're getting close. There should be request errors for PNGs left on the console. Search for the filenames and you'll end up in one of the JSONs you downloaded. Replace all `https://webstatic.hoyoverse.com/` with a blank. Then, you can regex `(?<="https://webstatic.hoyoverse.com/).+(?=")` and it'll find all of the asset urls. If you're on VS Code, you can `Ctrl+Shift+L` to select all of the matches. Paste them in `asset_downloader.py` and update the `url_prefix` variable to `https://webstatic.hoyoverse.com/`

One last thing, open the `styles_...css` files and regex `(?<=background-image: url\()images/.+(?=\))`. Add those files to `asset_downloader.py`, and set the prefix_url back to `https://act.hoyoverse.com/bh3/event/e20230724music/`

That should be all. If you hate yourself, you *can* make this run serverless by encoding all the assets in Base64 and then rewriting the code, like what I did for [e20230626preheating-cc1dq5](https://github.com/Honk-Web-Event-Archive/e20230626preheating-cc1dq5/tree/serverless), but that's unnecessary. I only made it serverless so it would work with Wallpaper Engine. 