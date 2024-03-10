# Commands

Commands are handled by the techcity [CLI](cli.md).

## fetch

```bash
techcity fetch
```

The `fetch` command pulls data from any API sources that are configured.
The raw data is normalized to fit the data definitions known to techcity.
The normalized data is persisted to the data storage directory.

The `fetch` command is idempotent and should be safe to execute multiple times.

## build

```bash
techcity build
```

The `build` command loads data from the storage directory
and renders the data into output HTML pages using the techcity templates.

## broadcast

```bash
techcity broadcast
```

The `broadcast` command loads broadcast schedules,
scans for pending broadcast messages,
and sends out any broadcasts to channels if any message is due.
