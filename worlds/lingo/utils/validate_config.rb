# Script to validate a level config file. This checks that the names used within
# the file are consistent. It also checks that the panel and door IDs mentioned
# all exist in the map file.
#
# Usage: validate_config.rb [config file] [ids path] [map file]

require 'set'
require 'yaml'

configpath = ARGV[0]
idspath = ARGV[1]
mappath = ARGV[2]

panels = Set["Countdown Panels/Panel_1234567890_wanderlust"]
doors = Set["Naps Room Doors/Door_hider_new1", "Tower Room Area Doors/Door_wanderer_entrance"]
paintings = Set[]

File.readlines(mappath).each do |line|
  line.match(/node name=\"(.*)\" parent=\"Panels\/(.*)\" instance/) do |m|
    panels.add(m[2] + "/" + m[1])
  end
  line.match(/node name=\"(.*)\" parent=\"Doors\/(.*)\" instance/) do |m|
    doors.add(m[2] + "/" + m[1])
  end
  line.match(/node name=\"(.*)\" parent=\"Decorations\/Paintings\" instance/) do |m|
    paintings.add(m[1])
  end
  line.match(/node name=\"(.*)\" parent=\"Decorations\/EndPanel\" instance/) do |m|
    panels.add("EndPanel/" + m[1])
  end
end

configured_rooms = Set["Menu"]
configured_doors = Set[]
configured_panels = Set[]
configured_panel_doors = Set[]

mentioned_rooms = Set[]
mentioned_doors = Set[]
mentioned_panels = Set[]
mentioned_panel_doors = Set[]
mentioned_sunwarp_entrances = Set[]
mentioned_sunwarp_exits = Set[]
mentioned_paintings = Set[]

door_groups = {}
panel_groups = {}

directives = Set["entrances", "panels", "doors", "panel_doors", "paintings", "sunwarps", "progression"]
panel_directives = Set["id", "required_room", "required_door", "required_panel", "colors", "check", "exclude_reduce", "tag", "link", "subtag", "achievement", "copy_to_sign", "non_counting", "hunt", "location_name"]
door_directives = Set["id", "painting_id", "panels", "item_name", "item_group", "location_name", "skip_location", "skip_item", "door_group", "include_reduce", "event", "warp_id"]
panel_door_directives = Set["panels", "item_name", "panel_group"]
painting_directives = Set["id", "display_name", "enter_only", "exit_only", "orientation", "required_door", "required", "required_when_no_doors", "move", "req_blocked", "req_blocked_when_no_doors"]

non_counting = 0

ids = YAML.load_file(idspath)

config = YAML.load_file(configpath)
config.each do |room_name, room|
  configured_rooms.add(room_name)

  used_directives = Set[]
  room.each_key do |key|
    used_directives.add(key)
  end
  diff_directives = used_directives - directives
  unless diff_directives.empty? then
    puts("#{room_name} has the following invalid top-level directives: #{diff_directives.to_s}")
  end

  (room["entrances"] || {}).each do |source_room, entrance|
    mentioned_rooms.add(source_room)

    entrances = []
    if entrance.kind_of? Hash
      entrances = [entrance]
    elsif entrance.kind_of? Array
      entrances = entrance
    end

    entrances.each do |e|
      if e.include?("door") then
        entrance_room = e.include?("room") ? e["room"] : room_name
        mentioned_rooms.add(entrance_room)
        mentioned_doors.add(entrance_room + " - " + e["door"])
      end
    end
  end

  (room["panels"] || {}).each do |panel_name, panel|
    unless panel_name.kind_of? String then
      puts "#{room_name} has an invalid panel name"
    end

    configured_panels.add(room_name + " - " + panel_name)

    if panel.include?("id")
      panel_ids = []
      if panel["id"].kind_of? Array
        panel_ids = panel["id"]
      else
        panel_ids = [panel["id"]]
      end

      panel_ids.each do |panel_id|
        unless panels.include? panel_id then
          puts "#{room_name} - #{panel_name} :::: Invalid Panel ID #{panel_id}"
        end
      end
    else
      puts "#{room_name} - #{panel_name} :::: Panel is missing an ID"
    end

    if panel.include?("required_room")
      required_rooms = []
      if panel["required_room"].kind_of? Array
        required_rooms = panel["required_room"]
      else
        required_rooms = [panel["required_room"]]
      end

      required_rooms.each do |required_room|
        mentioned_rooms.add(required_room)
      end
    end

    if panel.include?("required_door")
      required_doors = []
      if panel["required_door"].kind_of? Array
        required_doors = panel["required_door"]
      else
        required_doors = [panel["required_door"]]
      end

      required_doors.each do |required_door|
        other_room = required_door.include?("room") ? required_door["room"] : room_name
        mentioned_rooms.add(other_room)
        mentioned_doors.add("#{other_room} - #{required_door["door"]}")
      end
    end

    if panel.include?("required_panel")
      required_panels = []
      if panel["required_panel"].kind_of? Array
        required_panels = panel["required_panel"]
      else
        required_panels = [panel["required_panel"]]
      end

      required_panels.each do |required_panel|
        other_room = required_panel.include?("room") ? required_panel["room"] : room_name
        mentioned_rooms.add(other_room)
        mentioned_panels.add("#{other_room} - #{required_panel["panel"]}")
      end
    end

    unless panel.include?("tag") then
      puts "#{room_name} - #{panel_name} :::: Panel is missing a tag"
    end

    if panel.include?("non_counting") then
      non_counting += 1
    end

    bad_subdirectives = []
    panel.keys.each do |key|
      unless panel_directives.include?(key) then
        bad_subdirectives << key
      end
    end
    unless bad_subdirectives.empty? then
      puts "#{room_name} - #{panel_name} :::: Panel has the following invalid subdirectives: #{bad_subdirectives.join(", ")}"
    end

    unless ids.include?("panels") and ids["panels"].include?(room_name) and ids["panels"][room_name].include?(panel_name)
      puts "#{room_name} - #{panel_name} :::: Panel is missing a location ID"
    end
  end

  (room["doors"] || {}).each do |door_name, door|
    configured_doors.add("#{room_name} - #{door_name}")

    if door.include?("id")
      door_ids = []
      if door["id"].kind_of? Array
        door_ids = door["id"]
      else
        door_ids = [door["id"]]
      end

      door_ids.each do |door_id|
        unless doors.include? door_id then
          puts "#{room_name} - #{door_name} :::: Invalid Door ID #{door_id}"
        end
      end
    end

    if door.include?("painting_id")
      painting_ids = []
      if door["painting_id"].kind_of? Array
        painting_ids = door["painting_id"]
      else
        painting_ids = [door["painting_id"]]
      end

      painting_ids.each do |painting_id|
        unless paintings.include? painting_id then
          puts "#{room_name} - #{door_name} :::: Invalid Painting ID #{painting_id}"
        end
      end
    end

    if not door.include?("id") and not door.include?("painting_id") and not door.include?("warp_id") and not door["skip_item"] and not door["event"] then
      puts "#{room_name} - #{door_name} :::: Should be marked skip_item or event if there are no doors, paintings, or warps"
    end

    if door.include?("panels")
      door["panels"].each do |panel|
        if panel.kind_of? Hash then
          other_room = panel.include?("room") ? panel["room"] : room_name
          mentioned_panels.add("#{other_room} - #{panel["panel"]}")
        else
          other_room = panel.include?("room") ? panel["room"] : room_name
          mentioned_panels.add("#{room_name} - #{panel}")
        end
      end
    elsif not door["skip_location"]
      puts "#{room_name} - #{door_name} :::: Should be marked skip_location if there are no panels"
    end

    if door.include?("group")
      door_groups[door["group"]] ||= 0
      door_groups[door["group"]] += 1
    end

    bad_subdirectives = []
    door.keys.each do |key|
      unless door_directives.include?(key) then
        bad_subdirectives << key
      end
    end
    unless bad_subdirectives.empty? then
      puts "#{room_name} - #{door_name} :::: Door has the following invalid subdirectives: #{bad_subdirectives.join(", ")}"
    end

    unless door["skip_item"] or door["event"]
      unless ids.include?("doors") and ids["doors"].include?(room_name) and ids["doors"][room_name].include?(door_name) and ids["doors"][room_name][door_name].include?("item")
        puts "#{room_name} - #{door_name} :::: Door is missing an item ID"
      end
    end

    unless door["skip_location"] or door["event"]
      unless ids.include?("doors") and ids["doors"].include?(room_name) and ids["doors"][room_name].include?(door_name) and ids["doors"][room_name][door_name].include?("location")
        puts "#{room_name} - #{door_name} :::: Door is missing a location ID"
      end
    end
  end

  (room["panel_doors"] || {}).each do |panel_door_name, panel_door|
    configured_panel_doors.add("#{room_name} - #{panel_door_name}")

    if panel_door.include?("panels")
      panel_door["panels"].each do |panel|
        if panel.kind_of? Hash then
          other_room = panel.include?("room") ? panel["room"] : room_name
          mentioned_panels.add("#{other_room} - #{panel["panel"]}")
        else
          other_room = panel.include?("room") ? panel["room"] : room_name
          mentioned_panels.add("#{room_name} - #{panel}")
        end
      end
    else
      puts "#{room_name} - #{panel_door_name} :::: Missing panels field"
    end

    if panel_door.include?("panel_group")
      panel_groups[panel_door["panel_group"]] ||= 0
      panel_groups[panel_door["panel_group"]] += 1
    end

    bad_subdirectives = []
    panel_door.keys.each do |key|
      unless panel_door_directives.include?(key) then
        bad_subdirectives << key
      end
    end
    unless bad_subdirectives.empty? then
      puts "#{room_name} - #{panel_door_name} :::: Panel door has the following invalid subdirectives: #{bad_subdirectives.join(", ")}"
    end

    unless ids.include?("panel_doors") and ids["panel_doors"].include?(room_name) and ids["panel_doors"][room_name].include?(panel_door_name)
      puts "#{room_name} - #{panel_door_name} :::: Panel door is missing an item ID"
    end
  end

  (room["paintings"] || []).each do |painting|
    if painting.include?("id") and painting["id"].kind_of? String then
      unless paintings.include? painting["id"] then
        puts "#{room_name} :::: Invalid Painting ID #{painting["id"]}"
      end

      if mentioned_paintings.include?(painting["id"]) then
        puts "Painting #{painting["id"]} is mentioned more than once"
      else
        mentioned_paintings.add(painting["id"])
      end
    else
      puts "#{room_name} :::: Painting is missing an ID"
    end

    if painting["disable"] then
      # We're good.
      next
    end

    unless painting.include? "display_name" then
        puts "#{room_name} - #{painting["id"] || "painting"} :::: Missing display name"
    end

    if painting.include?("orientation") then
      unless ["north", "south", "east", "west"].include? painting["orientation"] then
        puts "#{room_name} - #{painting["id"] || "painting"} :::: Invalid orientation #{painting["orientation"]}"
      end
    else
      puts "#{room_name} :::: Painting is missing an orientation"
    end

    if painting.include?("required_door")
      other_room = painting["required_door"].include?("room") ? painting["required_door"]["room"] : room_name
      mentioned_doors.add("#{other_room} - #{painting["required_door"]["door"]}")

      unless painting["enter_only"] then
        puts "#{room_name} - #{painting["id"] || "painting"} :::: Should be marked enter_only if there is a required_door"
      end
    end

    bad_subdirectives = []
    painting.keys.each do |key|
      unless painting_directives.include?(key) then
        bad_subdirectives << key
      end
    end
    unless bad_subdirectives.empty? then
      puts "#{room_name} - #{painting["id"] || "painting"} :::: Painting has the following invalid subdirectives: #{bad_subdirectives.join(", ")}"
    end
  end

  (room["sunwarps"] || []).each do |sunwarp|
    if sunwarp.include? "dots" and sunwarp.include? "direction" then
      if sunwarp["dots"] < 1 or sunwarp["dots"] > 6 then
        puts "#{room_name} :::: Contains a sunwarp with an invalid dots value"
      end

      if sunwarp["direction"] == "enter" then
        if mentioned_sunwarp_entrances.include? sunwarp["dots"] then
          puts "Multiple #{sunwarp["dots"]} sunwarp entrances were found"
        else
          mentioned_sunwarp_entrances.add(sunwarp["dots"])
        end
      elsif sunwarp["direction"] == "exit" then
        if mentioned_sunwarp_exits.include? sunwarp["dots"] then
          puts "Multiple #{sunwarp["dots"]} sunwarp exits were found"
        else
          mentioned_sunwarp_exits.add(sunwarp["dots"])
        end
      else
        puts "#{room_name} :::: Contains a sunwarp with an invalid direction value"
      end
    else
      puts "#{room_name} :::: Contains a sunwarp without a dots and direction"
    end
  end

  (room["progression"] || {}).each do |progression_name, pdata|
    if pdata.include? "doors" then
      pdata["doors"].each do |door|
        if door.kind_of? Hash then
          mentioned_doors.add("#{door["room"]} - #{door["door"]}")
        else
          mentioned_doors.add("#{room_name} - #{door}")
        end
      end
    end

    if pdata.include? "panel_doors" then
      pdata["panel_doors"].each do |panel_door|
        if panel_door.kind_of? Hash then
          mentioned_panel_doors.add("#{panel_door["room"]} - #{panel_door["panel_door"]}")
        else
          mentioned_panel_doors.add("#{room_name} - #{panel_door}")
        end
      end
    end

    unless ids.include?("progression") and ids["progression"].include?(progression_name)
      puts "#{room_name} - #{progression_name} :::: Progression is missing an item ID"
    end
  end
end

errored_rooms = mentioned_rooms - configured_rooms
unless errored_rooms.empty? then
  puts "The following rooms are mentioned but do not exist: " + errored_rooms.to_s
end

errored_panels = mentioned_panels - configured_panels
unless errored_panels.empty? then
  puts "The following panels are mentioned but do not exist: " + errored_panels.to_s
end

errored_doors = mentioned_doors - configured_doors
unless errored_doors.empty? then
  puts "The following doors are mentioned but do not exist: " + errored_doors.to_s
end

errored_panel_doors = mentioned_panel_doors - configured_panel_doors
unless errored_panel_doors.empty? then
  puts "The following panel doors are mentioned but do not exist: " + errored_panel_doors.to_s
end

door_groups.each do |group,num|
  if num == 1 then
    puts "Door group \"#{group}\" only has one door in it"
  end

  unless ids.include?("door_groups") and ids["door_groups"].include?(group)
    puts "#{group} :::: Door group is missing an item ID"
  end
end

panel_groups.each do |group,num|
  if num == 1 then
    puts "Panel group \"#{group}\" only has one panel in it"
  end

  unless ids.include?("panel_groups") and ids["panel_groups"].include?(group)
    puts "#{group} :::: Panel group is missing an item ID"
  end
end

slashed_rooms = configured_rooms.select do |room|
  room.include? "/"
end
unless slashed_rooms.empty? then
  puts "The following rooms have slashes in their names: " + slashed_rooms.to_s
end

slashed_panels = configured_panels.select do |panel|
  panel.include? "/"
end
unless slashed_panels.empty? then
  puts "The following panels have slashes in their names: " + slashed_panels.to_s
end

slashed_doors = configured_doors.select do |door|
  door.include? "/"
end
unless slashed_doors.empty? then
  puts "The following doors have slashes in their names: " + slashed_doors.to_s
end

puts "#{configured_panels.size} panels (#{non_counting} non counting)"
