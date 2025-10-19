# 🎢 Archipelago Parkitect – AP World

This document describes how the **Parkitect AP World** integrates with the Archipelago multiworld randomizer.  
It covers configuration, item handling, scenarios, and how cross-game interactions work.

---

## ⚙️ Where is the Options Page?

You can find the **Parkitect Options Page** in your **Archipelago Client** under [here](../player-options)

This page contains all configuration fields necessary to generate your Parkitect world and export the appropriate `.apworld` or slot data file.

If everything looks correct, no special adjustments are required — the defaults work for most players.  
(You only need to modify this if you want to customize difficulty or behavior.)

---

## 🎲 What Does Randomization Affect?

The randomizer can affect almost every system inside Parkitect, bringing chaos and fun to your park management experience! 🎡

### Randomized Categories

#### 🧍 Player
- Starting **money**
- Attraction **speed modifiers** (5x, 7x, 9x)

#### 🎢 Attractions
- **Breakdowns**
- **Vouchers** that boost performance or guest appeal

#### 🍔 Stalls / Shops
- **Re-delivery of ingredients**
- **Cleaning jobs**
- **Vouchers**

#### 👷 Employees
- Can be **hired**, **trained**, or **made tired**


#### ☁️ Weather
- **Rainy**, **Cloudy**, **Sunny**, or **Stormy**  

#### 🧍‍♂️ Guests
- Can **spawn**, **lose money**, **gain money**, **vomit**, **vandalize**, or **leave unhappy**
- Their hunger, thirst, and tiredness levels may also change

#### 🗺️ Scenario
- Randomly adds **goals** with **custom rewards**

---

## 🌍 Which Items Can Appear in Another Player’s World?

Certain Parkitect items can be sent across the network and affect other players’ parks.  
Here’s what can appear in **other players’ worlds**:

| Category | Item | Description |
|-----------|------|-------------|
| **Player** | 💰 Money (+/-) | Changes player’s park funds |
| **Attractions** | ⚙️ Breakdowns | Random attraction malfunctions (excluding crashes & lightning strikes) |
| | 🎟️ Vouchers | Boost ride appeal or revenue |
| **Shops / Stalls** | 📦 Ingredient Re-Delivery | Triggers restocking |
| | 🧹 Cleaning Job | Assigns janitors |
| | 🎟️ Vouchers | Boost shop revenue |
| **Employees (Traps)** | 💤 Tired, 🧠 Training, 🧑‍🔧 Hiring | Modifies employee states |
| **Weather (Traps)** | 🌧️ Rainy / Stormy | Alters weather conditions |
| **Guests (Traps)** | 🧍 Spawning, 💀 Kill, 💸 Money (+/-), 🍔 Hungry, 🥤 Thirsty, 🚽 Toilet, 🤢 Vomit, 😡 Happiness, 😴 Tiredness, 🧨 Vandal | Alters guest states or spawns effects |

---

## 🎁 What Happens When the Player Receives an Item?

### 🧩 Planned / Work in Progress
When the player receives an **Archipelago item**, or completes a **challenge**,  
an **“Ingredient Package”** will appear at the **Depot**.  
A **Delivery Guy** (Handyman) will collect it and deliver it to the correct building.  
Once it arrives, the related AP item becomes **active/unlocked**.

> Example:  
> You receive a “Weather Control Voucher” → a package is delivered to the weather station → the new weather options unlock.

### ✅ Current Implementation
For now, items are **instantly applied** to the game state upon reception.  
Completing a challenge immediately **unlocks** its corresponding AP item.

---

## 🗺️ Available Scenarios

Currently included scenarios:

| Scenario Name | Description | Notes |
|----------------|--------------|-------|
| **Lakeside Green** | A relaxing park by the lake. Great starter map with balanced challenges. | Recommended for first-time AP runs |
| **Dusty Ridge Ranch** | A dry, rugged landscape perfect for testing weather effects. | More challenging terrain |

> 💡 More maps will be added over time — including community submissions!  
> You can request or submit new scenarios in the [GitHub repository](https://github.com/CrusherRL/AP_Parkitect_World/issues) or on Discord.

---

## 🧭 Scenario Rules (for Contributors)

If you want to submit your own Parkitect scenario for the AP World:

- Must include **all attraction and shop types**
- **Decorations** are optional (not randomized)
- Must have **one mandatory goal** (e.g., 100% happiness)
- Guests must **enter without pathfinding issues**
- Must be **balanced** and **fun**
- Should have **enough space** for building expansions
- The Park **must** work in vanilla

---

## 🧪 Testing & Compatibility

| Category | Status | Notes |
|-----------|---------|-------|
| **Operating Systems** | ✅ Tested on **Windows 10** | Not yet tested on **Linux** or **macOS** |
| **Multiplayer** | ⚠️ Not Tested / Likely Unsupported | Designed for single-player randomization |
| **Game Version** | ✅ Latest Steam build (as of Oct 2025) | Previous versions unverified |
| **Other Mods** | ⚙️ Tested with **Perspective Camera** | No known conflicts |
| **Performance** | ✅ Stable | No major FPS or crash issues detected |
| **Archipelago Connection** | ✅ Works with local & remote servers | Auto-connect supported |
| **AP World error on generation** | ⚙️ Sometimes won’t build | Try again xD happens around 1/7 |

---

## 💡 Future Ideas

- Proper **Delivery System** for AP items  
- Additional **Scenario maps** and themed challenges  

---

## ❤️ Credits

Created by **CrusherRL**
Special thanks to my friends who helped me with ideas, debugging and adding content!
Special thanks to the **Archipelago Community** for testing, feedback, and support!

---

🧩 *“Every park is a world — now it’s part of many.”*
