# This utility goes through the provided Lingo config and assigns item and
# location IDs to entities that require them (such as doors and panels). These
# IDs are output in a separate yaml file. If the output file already exists,
# then it will be updated with any newly assigned IDs rather than overwritten.
# In this event, all new IDs will be greater than any already existing IDs,
# even if there are gaps in the ID space; this is to prevent collision when IDs
# are retired.
#
# This utility should be run whenever logically new items or locations are
# required. If an item or location is created that is logically equivalent to
# one that used to exist, this utility should not be used, and instead the ID
# file should be manually edited so that the old ID can be reused.

require 'set'
require 'yaml'

configpath = ARGV[0]
outputpath = ARGV[1]

next_item_id = 444400
next_location_id = 444400

location_id_by_name = {}

old_generated = YAML.load_file(outputpath)
File.write(outputpath + ".old", old_generated.to_yaml)

if old_generated.include? "special_items" then
  old_generated["special_items"].each do |name, id|
    if id >= next_item_id then
      next_item_id = id + 1
    end
  end
end
if old_generated.include? "special_locations" then
  old_generated["special_locations"].each do |name, id|
    if id >= next_location_id then
      next_location_id = id + 1
    end
  end
end
if old_generated.include? "panels" then
  old_generated["panels"].each do |room, panels|
    panels.each do |name, id|
      if id >= next_location_id then
        next_location_id = id + 1
      end
      location_name = "#{room} - #{name}"
      location_id_by_name[location_name] = id
    end
  end
end
if old_generated.include? "doors" then
  old_generated["doors"].each do |room, doors|
    doors.each do |name, ids|
      if ids.include? "location" then
        if ids["location"] >= next_location_id then
          next_location_id = ids["location"] + 1
        end
      end
      if ids.include? "item" then
        if ids["item"] >= next_item_id then
          next_item_id = ids["item"] + 1
        end
      end
    end
  end
end
if old_generated.include? "door_groups" then
  old_generated["door_groups"].each do |name, id|
    if id >= next_item_id then
      next_item_id = id + 1
    end
  end
end
if old_generated.include? "panel_doors" then
  old_generated["panel_doors"].each do |room, panel_doors|
    panel_doors.each do |name, id|
      if id >= next_item_id then
        next_item_id = id + 1
      end
    end
  end
end
if old_generated.include? "panel_groups" then
  old_generated["panel_groups"].each do |name, id|
    if id >= next_item_id then
      next_item_id = id + 1
    end
  end
end
if old_generated.include? "progression" then
  old_generated["progression"].each do |name, id|
    if id >= next_item_id then
      next_item_id = id + 1
    end
  end
end

door_groups = Set[]
panel_groups = Set[]

config = YAML.load_file(configpath)
config.each do |room_name, room_data|
  if room_data.include? "panels"
    room_data["panels"].each do |panel_name, panel|
      unless old_generated.include? "panels" and old_generated["panels"].include? room_name and old_generated["panels"][room_name].include? panel_name then
        old_generated["panels"] ||= {}
        old_generated["panels"][room_name] ||= {}
        old_generated["panels"][room_name][panel_name] = next_location_id

        location_name = "#{room_name} - #{panel_name}"
        location_id_by_name[location_name] = next_location_id

        next_location_id += 1
      end
    end
  end
end

config.each do |room_name, room_data|
  if room_data.include? "doors"
    room_data["doors"].each do |door_name, door|
      if door.include? "event" and door["event"] then
        next
      end

      unless door.include? "skip_item" and door["skip_item"] then
        unless old_generated.include? "doors" and old_generated["doors"].include? room_name and old_generated["doors"][room_name].include? door_name and old_generated["doors"][room_name][door_name].include? "item" then
          old_generated["doors"] ||= {}
          old_generated["doors"][room_name] ||= {}
          old_generated["doors"][room_name][door_name] ||= {}
          old_generated["doors"][room_name][door_name]["item"] = next_item_id
  
          next_item_id += 1
        end

        if door.include? "group" and not door_groups.include? door["group"] then
          door_groups.add(door["group"])

          unless old_generated.include? "door_groups" and old_generated["door_groups"].include? door["group"] then
            old_generated["door_groups"] ||= {}
            old_generated["door_groups"][door["group"]] = next_item_id
    
            next_item_id += 1
          end
        end
      end

      unless door.include? "skip_location" and door["skip_location"] then
        location_name = ""
        if door.include? "location_name" then
          location_name = door["location_name"]
        elsif door.include? "panels" then
          location_name = door["panels"].map do |panel|
            if panel.kind_of? Hash then
              panel
            else
              {"room" => room_name, "panel" => panel}
            end
          end.sort_by {|panel| panel["room"]}.chunk {|panel| panel["room"]}.map do |room_panels|
            room_panels[0] + " - " + room_panels[1].map{|panel| panel["panel"]}.join(", ")
          end.join(" and ")
        end

        if location_id_by_name.has_key? location_name then
          old_generated["doors"] ||= {}
          old_generated["doors"][room_name] ||= {}
          old_generated["doors"][room_name][door_name] ||= {}
          old_generated["doors"][room_name][door_name]["location"] = location_id_by_name[location_name]
        elsif not (old_generated.include? "doors" and old_generated["doors"].include? room_name and old_generated["doors"][room_name].include? door_name and old_generated["doors"][room_name][door_name].include? "location") then
          old_generated["doors"] ||= {}
          old_generated["doors"][room_name] ||= {}
          old_generated["doors"][room_name][door_name] ||= {}
          old_generated["doors"][room_name][door_name]["location"] = next_location_id
  
          next_location_id += 1
        end
      end
    end
  end

  if room_data.include? "panel_doors"
    room_data["panel_doors"].each do |panel_door_name, panel_door|
      unless old_generated.include? "panel_doors" and old_generated["panel_doors"].include? room_name and old_generated["panel_doors"][room_name].include? panel_door_name then
        old_generated["panel_doors"] ||= {}
        old_generated["panel_doors"][room_name] ||= {}
        old_generated["panel_doors"][room_name][panel_door_name] = next_item_id

        next_item_id += 1
      end

      if panel_door.include? "panel_group" and not panel_groups.include? panel_door["panel_group"] then
        panel_groups.add(panel_door["panel_group"])

        unless old_generated.include? "panel_groups" and old_generated["panel_groups"].include? panel_door["panel_group"] then
          old_generated["panel_groups"] ||= {}
          old_generated["panel_groups"][panel_door["panel_group"]] = next_item_id

          next_item_id += 1
        end
      end
    end
  end

  if room_data.include? "progression"
    room_data["progression"].each do |progression_name, pdata|
      unless old_generated.include? "progression" and old_generated["progression"].include? progression_name then
        old_generated["progression"] ||= {}
        old_generated["progression"][progression_name] = next_item_id

        next_item_id += 1
      end
    end
  end
end

File.write(outputpath, old_generated.to_yaml)

puts "Next item ID: #{next_item_id}"
puts "Next location ID: #{next_location_id}"
