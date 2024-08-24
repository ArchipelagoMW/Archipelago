import { FlagSet, FlagLogic } from './flags.js'

async function upconvertBinaryFlags(binaryFlagString)
{
    let obj = await import("./flagUpconverter.js");
    return obj.default(binaryFlagString);
}

class InitializationPanel extends React.Component
{
    constructor(props)
    {
        super(props);
        this.handleButtonClick = this.handleButtonClick.bind(this);
        this.handleApplyFlags = this.handleApplyFlags.bind(this);

        this.state = {mode : (this.props.initialFlagString ? 'input' : null), error : null, warnings : null};
    }

    componentDidMount()
    {
        if (this.props.initialFlagString)
        {
            this.handleApplyFlags(this.props.initialFlagString, false);
        }
    }

    handleButtonClick(index)
    {
        if (index == 2)
        {
            this.setState({mode : null}, () => { this.handleApplyFlags("") });
        }
        else
        {
            this.setState({mode : (index == 0 ? 'presets' : 'input')});
        }
    }

    handleApplyFlags(flagString, scroll=true)
    {
        let flags = new FlagSet();
        try
        {
            flags.load(flagString);
        }
        catch (err)
        {
            // if the flag string is binary and failed to load, attempt an upconversion
            if (flagString.startsWith('b'))
            {
                upconvertBinaryFlags(flagString)
                    .then( ({flagset, details}) => {
                        let warnings = ["This flag string is from a previous version of Free Enterprise; we've attempted to set the closest matching flags with the current version below."].concat(details);
                        this.setState({error: null, warnings: warnings}, () => { 
                            this.props.onApplyFlags(flagset);
                            if (scroll)
                            {
                                document.getElementById("flagStringWarnings").scrollIntoView({behavior: 'smooth'});
                            }
                        });                        
                    })
                    .catch( (e) => {
                        this.setState({error : "Error loading flag string: " + e.message});
                    });
                return;
            }

            this.setState({error : "Error loading flag string: " + err.message});
            return;
        }

        this.setState({error: null, warnings: null}, () => { 
            this.props.onApplyFlags(flags); 
            if (scroll)
            {
                document.getElementById("flagEditor").scrollIntoView({behavior: 'smooth'});
            }
        });
    }

    render()
    {
        let control = null;
        if (this.state.mode === 'presets')
        {
            control = React.createElement(PresetPanel, {spec: this.props.presets, onApply: this.handleApplyFlags});
        }
        else if (this.state.mode === 'input')
        {
            control = React.createElement(FlagStringInputPanel, {initialFlagString: this.props.initialFlagString, onApply: this.handleApplyFlags});
        }

        let error = null;
        if (this.state.error)
        {
            error = React.createElement("div", {className: "error"}, this.state.error);
        }

        let warnings = null;
        if (this.state.warnings && this.state.warnings.length > 0)
        {
            warnings = React.createElement("div", {className: "warnings", id: "flagStringWarnings"}, 
                ...this.state.warnings.map( (warning) => React.createElement("div", { className: "warning" }, warning) )
                );
        }

        return React.createElement("div", {className: "initializationPanel"},
            React.createElement(InitializationButtons, {buttons : ["Choose Preset", "Input Flag String", "Build From Scratch"], onButtonClick: this.handleButtonClick}),
            control,
            error,
            warnings
        );
    }
}

class InitializationButtons extends React.Component
{
    constructor(props)
    {
        super(props);
    }

    render()
    {
        return React.createElement("div", {className: "initializationButtons"},
            this.props.buttons.map(
                (name, idx) => React.createElement(
                    "div", {key: name, className: "initializationButton", onClick: () => {this.props.onButtonClick(idx);}}, name
                    )
            )
        );
    }
}

class PresetPanel extends React.Component
{
    constructor(props)
    {
        super(props);
        this.handleCategorySelect = this.handleCategorySelect.bind(this);

        this.state = {
            selectedCategory: null
        };
    }

    handleCategorySelect(category)
    {
        this.setState({selectedCategory: category});
    }

    render()
    {
        let children = [];
        if (this.props.spec === null)
        {
            children.push(React.createElement("div", {className: "spinner"}));
        }
        else
        {
            let selectedCategory = this.state.selectedCategory;
            if (!selectedCategory && this.props.spec)
            {
                selectedCategory = this.props.spec.filter((item) => item.presets)[0];
            }

            children = [
                React.createElement(PresetCategoriesMenu, {
                    spec: this.props.spec,
                    selectedCategory: selectedCategory,
                    onCategorySelect: this.handleCategorySelect
                }),
                React.createElement(PresetOptions, {
                    options: selectedCategory.presets,
                    external: selectedCategory.external,
                    onPresetSelected: this.props.onApply
                })
            ];
        }

        return React.createElement("div", {className: "initializationSubPanel presets"}, ...children);
    }
}

class PresetCategoriesMenu extends React.Component
{
    render()
    {
        return React.createElement("div", {className: "presetCategories"},
            this.props.spec.map((menuItem, index) => {
                if (menuItem.header)
                {
                    return React.createElement("div", {className: "presetHeader", key: index}, menuItem.header);
                }
                else
                {
                    let isSelected = (menuItem.category === this.props.selectedCategory.category);
                    return React.createElement("div", {
                        className: "presetCategory" + (isSelected ? " selected" : ""),
                        key: index,
                        onClick: () => this.props.onCategorySelect(menuItem)
                    }, menuItem.category);
                }
            })
        );
    }
}

class PresetOptions extends React.Component
{
    render()
    {
        return React.createElement("div", {className: "presetOptions"},
            ...this.props.options.map((preset) => React.createElement(PresetBox, {...preset, external: this.props.external, onClick: this.props.onPresetSelected}))
        );
    }
}

class PresetBox extends React.Component
{
    render()
    {
        return React.createElement("div", {className: "preset", onClick: () => {this.props.onClick(this.props.flags);}},
            React.createElement("div", {className: "presetName"}, this.props.name),
            ( this.props.external
              ? React.createElement("div", {className: "presetDescription"}, React.createElement("p", {}, this.props.description))
              : React.createElement("div", {
                  className: "presetDescription", 
                  dangerouslySetInnerHTML: {__html: this.props.description}
                }
            )),
            React.createElement("div", {className: "presetFlags"}, this.props.flags)
        );
    }
}

class FlagStringInputPanel extends React.Component
{
    constructor(props)
    {
        super(props);
        this.handleTextChange = this.handleTextChange.bind(this);
        let flagString = this.props.initialFlagString;
        /*
        if (flagString && flagString.startsWith("b"))
        {
            let flagset = new FlagSet();
            flagset.load(flagString);
            flagString = flagset.to_string();
        }
        */
        this.state = {flags: flagString, showApply : !(this.props.initialFlagString)};
    }

    handleTextChange(e)
    {
        this.setState({flags: e.target.value, showApply: true});
    }

    render()
    {
        return React.createElement("div", {},
            React.createElement("div", {className: "initializationSubPanel"},
                React.createElement("textarea", {className: "flagStringInput" + (this.state.showApply ? "" : " initial"), spellCheck: false, placeholder: "(enter flag string)", onChange : this.handleTextChange, defaultValue: this.state.flags}),
                ),
            (this.state.showApply 
                ? React.createElement("div", {className: "applyFlagsButton button", onClick: () => { this.props.onApply(this.state.flags); }}, "Apply Flags") 
                : null
            )
        );
    }
}

//--------------------------------------------

const FlagEditContext = React.createContext({enabled: {}, applyEdits: (edits) => {}});

class FlagEditor extends React.Component
{
    constructor(props)
    {
        super(props);

        this.handleEdits = this.handleEdits.bind(this);
        this.handleFlagReset = this.handleFlagReset.bind(this);

        this.props.flagResetNotifier.register(this.handleFlagReset);

        let flags = new FlagSet();
        if (this.props.initialFlagString)
        {
            flags.load(this.props.initialFlagString);
        }

        let enabledItems = this.calculateEnabledItems(flags);
        this.state = {enabledItems : enabledItems};
        this.handleFlagUpdate(flags);
    }

    handleFlagReset(flags)
    {
        let enabledItems = this.calculateEnabledItems(flags);
        this.setState({enabledItems : enabledItems});
        this.handleFlagUpdate(flags);
    }

    calculateEnabledItems(flags)
    {
        let enabledItems = {};
        flags.get_list().forEach((flag) => {enabledItems[flag] = true;});
        this.calculateRequiredContainers(enabledItems).forEach((flag) => {enabledItems[flag] = true;});
        return enabledItems;
    }

    calculateRequiredContainers(enabledFlags)
    {
        let requiredContainers = {};

        let walkSpecRecursive = (spec, branch) => {
            if (spec.controls)
            {
                spec.controls.forEach((subspec) => { walkSpecRecursive(subspec, branch); });
            }
            else if (spec.flag.startsWith('@') || enabledFlags[spec.flag])
            {
                if (spec.flag.startsWith('@'))
                {
                    branch = branch.concat([spec.flag]);
                }
                else if (enabledFlags[spec.flag])
                {
                    branch.forEach((flag) => {requiredContainers[flag] = true;});
                }

                if (spec.subcontrols)
                {
                    spec.subcontrols.forEach((subspec) => { walkSpecRecursive(subspec, branch); });
                }
            }
        };

        this.props.spec.forEach((section) => {walkSpecRecursive(section, []);});

        return Object.keys(requiredContainers);
    }

    handleEdits(edits)
    {
        let enabledItems = this.state.enabledItems;
        let flagsDirty = false;
        Object.keys(edits).forEach(
            (flag) => {
                let action = edits[flag];
                if (action == 'set')
                {
                    enabledItems[flag] = true;
                }
                else
                {
                    delete enabledItems[flag];
                }
            });

        this.setState({enabledItems: enabledItems});

        // Calculate true flagset based on visible toggles
        let visibleFlags = [];
        let walkSpecRecursive = (specs) => {
            specs.forEach((spec) => {
                if (enabledItems[spec.flag] || spec.type == 'select')
                {
                    if (!spec.flag.startsWith("@"))
                    {
                        visibleFlags.push(spec.flag);
                    }
                    if (spec.subcontrols)
                    {
                        walkSpecRecursive(spec.subcontrols);
                    }
                }
            })
        };
        this.props.spec.forEach((section) => {walkSpecRecursive(section.controls);});

        let trueFlags = new FlagSet();
        visibleFlags.forEach((flag) => { trueFlags.set(flag); });
        this.handleFlagUpdate(trueFlags);
    }

    handleFlagUpdate(flags)
    {
        if (this.props.onFlagsChanged)
        {
            this.props.onFlagsChanged(flags);
        }
    }

    render()
    {
        let sections = this.props.spec.map((section) => React.createElement(FlagSection, {key: section.title, spec: section}));

        let contextValue = {
            enabledItems : this.state.enabledItems,
            applyEdits : this.handleEdits
            };

        return React.createElement(FlagEditContext.Provider, {value : contextValue},
            React.createElement("div", {className: "flagEditor"}, sections)
            );
    }
}

class FlagSection extends React.Component
{
    render()
    {
        return React.createElement("div", {className: "flagSection " + this.props.spec.title.toLowerCase().replace(/[^a-z]/, '')},
            React.createElement("div", {className: "sectionTitle"}, this.props.spec.title),
            React.createElement(FlagControlList, {spec: this.props.spec.controls})
            );
    }
}

class FlagControlList extends React.Component
{
    render()
    {
        let controls = this.props.spec.map(
            (control) => {
                let props = {key: control.flag, spec: control};
                if (control.type == 'select')
                {
                    return React.createElement(FlagSelector, props);
                }
                else if (control.type == 'separator')
                {
                    return React.createElement("div", {key: props.key, className: "separator"});
                }
                else
                {
                    return React.createElement(FlagControl, props);
                }
            });
        return React.createElement("div", {className: "flagControlList" + (this.props.compact ? " compact" : "")}, controls);
    }
}

class FlagSelector extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = {menuOpen : false, flag : null};
        this.handleClick = this.handleClick.bind(this);
        this.handleMenuClick = this.handleMenuClick.bind(this);
        this.handleDismissClick = this.handleDismissClick.bind(this);
    }

    handleClick(e)
    {
        this.setState({menuOpen : true});
    }

    handleMenuClick(spec)
    {
        let edits = {};
        this.props.spec.subcontrols.forEach((subspec) => {
            edits[subspec.flag] = (spec.flag === subspec.flag ? 'set' : 'unset');
        });

        this.setState({menuOpen : false}, 
            () => { 
                this.context.applyEdits(edits) 
            }
        );
    }

    handleDismissClick(e)
    {
        this.setState({menuOpen : false});
    }

    render()
    {
        let activeControl = null;
        
        for (let i = 0; i < this.props.spec.subcontrols.length; i++)
        {
            let subspec = this.props.spec.subcontrols[i];
            if (this.context.enabledItems[subspec.flag])
            {
                activeControl = React.createElement(FlagControl, {spec: subspec, icon: "select", onClick: this.handleClick});
                break;
            }
        }

        if (activeControl === null)
        {
            // show default control
            activeControl = React.createElement("div", {className:"flagSelector"},
                React.createElement(FlagButton, {spec: this.props.spec, icon: "select", onClick: this.handleClick}));
        }

        let selectors = this.props.spec.subcontrols.map(
                (subspec) => React.createElement(FlagButton, 
                    {
                        spec: subspec, 
                        key: subspec.flag,
                        selected: this.context.enabledItems[subspec.flag],
                        onClick: this.handleMenuClick
                    })
                );
        if (!this.props.spec.important)
        {
            selectors.unshift(React.createElement(FlagButton, {spec:this.props.spec, icon: "select", key:this.props.spec.flag, onClick: this.handleMenuClick}));
        }

        let menu = React.createElement("div", {className: "flagSelectorMenu" + (this.state.menuOpen ? " open" : "")}, selectors);

        let dismisser = null;
        if (this.state.menuOpen)
        {
            dismisser = React.createElement("div", {className:"menuDismissOverlay", onClick:this.handleDismissClick});
        }

        return React.createElement("div", {
                className:"flagSelectorContainer" + (this.props.spec.important ? " important" : "")
            }, 
            dismisser, menu, activeControl);
    }
}
FlagSelector.contextType = FlagEditContext;

class FlagControl extends React.Component
{
    constructor(props)
    {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(spec)
    {
        if (this.props.onClick)
        {
            this.props.onClick(spec);
        }
        else
        {
            let edits = {};
            edits[this.props.spec.flag] = (this.context.enabledItems[this.props.spec.flag] ? 'unset' : 'set');
            this.context.applyEdits(edits);
        }
    }

    render()
    {
        let subsection = null;
        if (this.props.spec.description || this.props.spec.subcontrols)
        {
            let description = null;
            if (this.props.spec.description)
            {
                description = React.createElement("div", {
                    className:"flagDescription", 
                    dangerouslySetInnerHTML:{__html:this.props.spec.description}}
                );
            }

            let subcontrols = null;
            if (this.props.spec.subcontrols)
            {
                subcontrols = React.createElement(FlagControlList, {spec: this.props.spec.subcontrols, compact: this.props.spec.compact});
            }

            subsection = React.createElement("div", {className:"flagSubsection"}, 
                description,
                subcontrols
            );
        }

        let isContainer = this.props.spec.flag.startsWith('@');

        let isSelected = this.context.enabledItems[this.props.spec.flag];

        return React.createElement("div", 
                {
                    className:"flagControl" 
                              + (isSelected ? " selected" : "") 
                              + (this.props.spec.hard ? " hard" : "")
                              + (isContainer ? " container" : "")
                },
                React.createElement(FlagButton, {
                    spec: this.props.spec, 
                    selected: isSelected, 
                    icon: this.props.icon,
                    onClick: this.handleClick}),
                subsection
            );
    }
}
FlagControl.contextType = FlagEditContext;

class FlagButton extends React.Component
{
    constructor(props)
    {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(e)
    {
        e.preventDefault();
        if (this.props.onClick)
        {
            this.props.onClick(this.props.spec);
        }
    }

    render()
    {
        let isContainer = this.props.spec.flag.startsWith('@');

        let iconLabel = "";
        if (this.props.isSelector || this.props.icon == "select")
        {
            iconLabel = "\u2263";
        }
        else if (isContainer)
        {
            iconLabel = (this.props.selected ? "..." : "");
            //iconLabel = (this.props.selected ? "\u25bf" : "\u25b9");
        }
        else if (this.props.selected && !this.props.spec.null)
        {
            iconLabel = "\u2713";
        }

        let flagName = null;
        if (!isContainer)
        {
            flagName = React.createElement("div", 
                {className:"flagName" + (isContainer ? " container" : "")}, 
                (isContainer ? "..." : this.props.spec.flag));
        }

        return React.createElement("div", 
            {
                className: ("flagButton" 
                    + (this.props.selected ? " selected" : "") 
                    + (this.props.spec.hard ? " hard" : "") 
                    + (this.props.spec.null ? " null" : "")
                    ),
                onClick: this.handleClick
            },
            React.createElement("div", {className:"flagIcon"}, iconLabel),
            React.createElement("div", {className:"flagTitle"}, this.props.spec.title),
            flagName
        );
    }    
}

//-------------------------------------------
class FlagLogicLogList extends React.Component
{
    render()
    {
        if (this.props.log.length == 0)
        {
            return null;
        }
        else
        {
            let logItems = this.props.log.map( (log) => React.createElement("div", {className: log[0]}, log[1]) );
            return React.createElement("div", {className: "list"},
                ...logItems
                );
        }
    }
}

//-------------------------------------------
class GenerateButton extends React.Component
{
    constructor(props)
    {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick()
    {
        generate();
    }

    render()
    {
        if (this.props.enabled)
        {
            return React.createElement("div", {id:"generateButton", onClick:this.handleClick}, "Generate");
        }
        else
        {
            return "There are logical error(s) in your flags; please correct them before proceeding.";
        }
    }
}

//-------------------------------------------

// yuck... next time I should Think Harder In React
class Notifier
{
    constructor()
    {
        this.handlers = [];
    }

    register(handler)
    {
        this.handlers.push(handler);
    }

    notify(arg)
    {
        this.handlers.forEach((handler) => { handler(arg); });
    }
}

class App extends React.Component
{
    constructor(props)
    {
        super(props);

        this.handleFlagsReset = this.handleFlagsReset.bind(this);
        this.handleFlagsChanged = this.handleFlagsChanged.bind(this);

        this.flagResetNotifier = new Notifier();
        this.flagLogic = new FlagLogic();

        this.state = {
            flagLogicLog : [], 
            flagString : '', 
            binaryFlagString : '',
            flagsValid : true,
            presets: null
        };

        this.fetchPresets();
    }

    handleFlagsReset(flags)
    {
        this.flagResetNotifier.notify(flags);
    }

    handleFlagsChanged(flags)
    {
        let log = this.flagLogic.fix(flags);
        let hasError = false;
        log.forEach( (item) => {
            hasError = hasError || (item[0] == 'error')
        });
        this.setState({
            flagLogicLog : log,
            flagString : flags.to_string(), 
            binaryFlagString : flags.to_binary(),
            flagsValid : !hasError
        });
    }

    async fetchPresets()
    {
        let r = await fetch('/presets');
        if (r.status >= 200 && r.status < 300)
        {
            this.setState({presets: await r.json()});
        }
    }

    render()
    {
        let editorInitialFlagString = ""; // TODO
        if (this.props.initialFlagString)
        {
            editorInitialFlagString = null;
        }

        return React.createElement(React.Fragment, {},
            ReactDOM.createPortal(
                React.createElement(InitializationPanel, {
                    initialFlagString: this.props.initialFlagString, 
                    presets: this.state.presets, 
                    onApplyFlags: this.handleFlagsReset
                }), 
                document.getElementById("initializationContainer")
            ),
            ReactDOM.createPortal(
                React.createElement(FlagEditor, {
                    spec: this.props.uispec, 
                    initialFlagString: editorInitialFlagString, 
                    onFlagsChanged: this.handleFlagsChanged,
                    flagResetNotifier: this.flagResetNotifier
                }),
                document.getElementById("flagEditor")
            ),
            ReactDOM.createPortal(
                React.createElement(FlagLogicLogList, {log : this.state.flagLogicLog}), 
                document.getElementById("flagLogicLogDisplay")
            ),
            ReactDOM.createPortal(this.state.flagString, document.getElementById("flagStringDisplay")),
            ReactDOM.createPortal(this.state.binaryFlagString, document.getElementById("binaryFlagStringDisplay")),
            ReactDOM.createPortal(
                React.createElement(GenerateButton, {enabled : this.state.flagsValid}),
                document.getElementById("generateButtonContainer")
            ),
        );
    }
}

ReactDOM.render(
    React.createElement(App, {uispec:FLAG_UISPEC, initialFlagString:DEFAULT_FLAGS}),
    document.getElementById("appContainer")
);
