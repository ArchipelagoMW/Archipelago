# Script to validate a level config file. This checks that the names used within
# the file are consistent. It also checks that the panel and door IDs mentioned
# all exist in the map file.
#
# Usage: validate_config.rb [config file] [map file]

require 'set'
require 'yaml'

configpath = ARGV[0]
mappath = ARGV[1]

panels = Set[]
doors = Set[]
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

mentioned_rooms = Set[]
mentioned_doors = Set[]
mentioned_panels = Set[]

config = YAML.load_file(configpath)
config.each do |room_name, room|
  configured_rooms.add(room_name)

  (room["entrances"] || {}).each do |source_room, entrance|
    mentioned_rooms.add(source_room)

    entrances = []
    if entrance.kind_of? Hash
      entrances = [entrance]
    elsif entrance.kind_of? Array
      entrances = entrance
    end

    entrances.each do |e|
      entrance_room = e.include?("room") ? e["room"] : room_name
      mentioned_rooms.add(entrance_room)
      mentioned_doors.add(entrance_room + " - " + e["door"])
    end
  end

  (room["panels"] || {}).each do |panel_name, panel|
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
        mentioned_doors.add("#{other_room} - #{required_door["door"]}")
      end
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

    if not door.include?("id") and not door.include?("painting_id") and not door["skip_item"] then
      puts "#{room_name} - #{door_name} :::: Should be marked skip_item if there are no doors or paintings"
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
  end
end

errored_rooms = mentioned_rooms - configured_rooms
unless errored_rooms.empty? then
  puts "The folloring rooms are mentioned but do not exist: " + errored_rooms.to_s
end

errored_panels = mentioned_panels - configured_panels
unless errored_panels.empty? then
  puts "The folloring panels are mentioned but do not exist: " + errored_panels.to_s
end

errored_doors = mentioned_doors - configured_doors
unless errored_doors.empty? then
  puts "The folloring doors are mentioned but do not exist: " + errored_doors.to_s
end
