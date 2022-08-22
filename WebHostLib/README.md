# WebHost

## Contribution Guidelines
**Thank you for your interest in contributing to the Archipelago website!**  
Much of the content on the website is generated automatically, but there are some things
that need a personal touch. For those things, we rely on contributions from both the core
team and the community. The current primary maintainer of the website is Farrak Kilhn.
He may be found on Discord as `Farrak Kilhn#0418`, or on GitHub as `LegendaryLinux`.

### Small Changes
Little changes like adding a button or a couple new select elements are perfectly fine.
Tweaks to style specific to a PR's content are also probably not a problem. For example, if
you build a new page which needs two side by side tables, and you need to write a CSS file
specific to your page, that is perfectly reasonable.

### Content Additions
Once you develop a new feature or add new content the website, make a pull request. It will
be reviewed by the community and there will probably be some discussion around it. Depending
on the size of the feature, and if new styles are required, there may be an additional step
before the PR is accepted wherein Farrak works with the designer to implement styles.

### Restrictions on Style Changes
A professional designer is paid to develop the styles and assets for the Archipelago website.
In an effort to maintain a consistent look and feel, pull requests which *exclusively*
change site styles are rejected. Please note this applies to code which changes the overall
look and feel of the site, not to small tweaks to CSS for your custom page. The intention
behind these restrictions is to maintain a curated feel for the design of the site. If
any PR affects the overall feel of the site but includes additive changes, there will
likely be a conversation about how to implement those changes without compromising the
curated site style. It is therefore worth noting there are a couple files which, if
changed in your pull request, will cause it to draw additional scrutiny.

These closely guarded files are:
- `globalStyles.css`
- `islandFooter.css`
- `landing.css`
- `markdown.css`
- `tooltip.css`

### Site Themes
There are several themes available for game pages. It is possible to request a new theme in
the `#art-and-design` channel on Discord. Because themes are created by the designer, they
are not free, and take some time to create. Farrak works closely with the designer to implement
these themes, and pays for the assets out of pocket. Therefore, only a couple themes per year
are added. If a proposed theme seems like a cool idea and the community likes it, there is a
good chance it will become a reality.
