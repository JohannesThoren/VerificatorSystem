<!--
 Copyright 2022 Johannes Thorén. All rights reserved.
 Use of this source code is governed by a BSD-style
 license that can be found in the LICENSE file.
-->
# The Api
There is a small api for getting links.

#### Syntax (using discord id's)
```
GET: /api/<token>/get/link/discordid/<discord_id>
```

#### Syntax (using steam id's)
```
GET: /api/<token>/get/link/steamid/<steamid>
```

## Response
Both requests will return the same response
```JSON
{
      "link": {
            "discord_id": "The ID",
            "steam_id": "The ID"
      }
}
```