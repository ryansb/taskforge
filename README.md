# taskforge

Powered by [taskw](https://github.com/ralphbean/taskw)

# Configuration

The config is in YAML format, and looks like this (delete `#` prefixed lines
`#`)

```
logging:
  level: DEBUG
  file: ''

plugins:
  - nickname: Emailotron
    # the entrypoint for your plugin needs to inherit from
    # `taskforge.plugins.Base`
    entrypoint: emailotron:Emailer
    # plugins are run in ascending weight order. Plugins with the same
    # weight may be run in any order. The default value for weight is 100.
    weight: 0
    enabled: false
    # plugins are initialized with the contents of this options field
    options:
      some: thing
```

# Plugins

Yes, that's right, you can build your own plugins! Just add your plugin to the
list in the plugins section and set `enabled: true`.

# License

Taskforge is made available under the GNU Affero General Public License, see
LICENSE.txt for details.
