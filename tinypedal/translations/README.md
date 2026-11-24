# TinyPedal interface translations

Choose **Config → Application → Language (Restart Required)**, save, then select
**Window → Restart TinyPedal**. The default is English. Untranslated entries use
the original English text.

`ui_*.ts` contains Qt interface strings. `labels_*.ts` contains dynamic labels
looked up by configuration or module key, along with common Qt button labels.
Keep these keys and any named placeholders intact when editing translations.

With the Qt for Python tools installed, run these commands from the repository
root to refresh the extracted strings and rebuild the Simplified Chinese catalogs.

```sh
pyside6-lupdate -extensions py -locations none tinypedal/ui -ts tinypedal/translations/ui_zh_CN.ts
pyside6-lrelease tinypedal/translations/ui_zh_CN.ts tinypedal/translations/labels_zh_CN.ts
```

Keep the generated `.qm` files with their `.ts` sources so source and packaged
builds can load translations without installing Qt Linguist.
