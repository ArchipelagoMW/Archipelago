
import contextlib

from .. import _common
from .. import soundBank
from .. import soundSequence


_MONO = soundSequence.MonoPolySequenceEvent.Value.MONO
_POLY = soundSequence.MonoPolySequenceEvent.Value.POLY


def minifyByEvents(eventsIter, sbnk, swars=None):
    """
    Minify the given SBNK and optionally SWARs.

    This is a low-level minification function; before you consider using
    it, check whether you can instead use a higher-level variation:

    - minifyBySseq()
    - minifyBySseqs()
    - SSEQMusic.minify()

    eventsIter is an iterator over all events that use the SBNK. This
    list must be exhaustive; if not, SSEQs you omit won't be updated to
    reflect changes in instrument IDs, which will result in broken
    music. Also, too many instruments might be deleted.

    sbnk is the SBNK to be minified.

    swars is the list of (up to four) SWARs that the SBNK uses. If
    provided, anything within them that the SBNK doesn't use (after it's
    been minified) will be removed. This is optional.

    Note that minifying SWARs is usually the most important part. (SBNKs
    are generally tiny in comparison.)

    Doesn't return anything; the objects you pass as params are
    modified.

    Warning: you should only use this after you're completely done
    editing your sseq (programmatically or otherwise).

    Warning 2: this is a one-way operation that strips away all
    instruments you're not using (and even unused aspects of the
    instruments you do use). Don't delete the original after you use
    this, because it's not very easy to undo this.

    Note to whoever's cleaning up this documentation: those warnings
    should be copypasted (and modified as needed) to the other minify
    functions that build on this one.

    .. todo::
        Another optimization that can be done is combining consecutive
        rests. You have to check that they're not a jump target of some
        sort first, though! (including implicit jumps defined by track
        start events and the like)

        Also, something else that's a bit easier is removing instruments
        that are emptied of all of their notes (e.g. they're referenced
        but not actually used).

        Also, while you can't indiscriminately delete raw-data events,
        you can check for any that immediately follow a (non-conditional)
        end-of-track or jump event and are not a jump target, and delete
        those. This covers the very common case of needlessly ending a
        track with 0xFFFF.

        Also, each of these optimizations should really be its own
        function, since this code is getting kind of complicated.
    """

    # This used to be a parameter defaulting to False, since it was
    # unreliable and could break songs; however, it's stable enough now
    # that it shouldn't be publicly exposed. It'll still be here as a
    # constant for debugging purposes, though.
    MINIFY_INSTRUMENTS=True

    events = list(eventsIter)

    # Remove unused entries in SBNK relative to SSEQ
    usedInsts = set()
    playedNotes = {}
    currentInstrument = None
    for e in events:
        if isinstance(e, soundSequence.InstrumentSwitchSequenceEvent):
            currentInstrument = e.instrumentID
            usedInsts.add(currentInstrument)
            if currentInstrument not in playedNotes:
                playedNotes[currentInstrument] = set()
        elif isinstance(e, soundSequence.NoteSequenceEvent):
            if currentInstrument is not None:
                playedNotes[currentInstrument].add(e.type)
    usedInsts = sorted(usedInsts)
    sbnk.instruments = [sbnk.instruments[num] for num in usedInsts]
    playedNotesPerInst = [playedNotes[num] for num in usedInsts]
    for e in events:
        if isinstance(e, soundSequence.InstrumentSwitchSequenceEvent):
            e.instrumentID = usedInsts.index(e.instrumentID)

    # (and instruments that were useless in the first place)
    sbnk.inaccessibleInstruments.clear()

    # Remove unused entries in SWAR relative to SBNK
    usedWaves = set()
    for inst, notes in zip(sbnk.instruments, playedNotesPerInst):
        if isinstance(inst, soundBank.SingleNoteInstrument):
            usedWaves.add((inst.noteDefinition.waveArchiveIDID, inst.noteDefinition.waveID))
        elif isinstance(inst, soundBank.RangeInstrument):
            noteNum = inst.firstPitch - 1
            for d in inst.noteDefinitions:
                noteNum += 1
                if MINIFY_INSTRUMENTS and (noteNum not in notes):
                    continue
                usedWaves.add((d.waveArchiveIDID, d.waveID))
        elif isinstance(inst, soundBank.RegionalInstrument):
            low = 0
            for reg in inst.regions:
                if MINIFY_INSTRUMENTS:
                    # Try to find the note; if it can't be found,
                    # skip this swav
                    for i in range(low, reg.lastPitch + 1):
                        if i in notes:
                            break
                    else:
                        continue
                usedWaves.add((reg.noteDefinition.waveArchiveIDID, reg.noteDefinition.waveID))
                low = reg.lastPitch + 1
    usedWaves = sorted(usedWaves, key=lambda e: e[0] * 99999999 + e[1])

    for swarNum, swar in enumerate(swars):
        newWaves = []
        for (swarNum2, swavNum) in usedWaves:
            if swarNum != swarNum2: continue
            newWaves.append(swar.waves[swavNum])
        swar.waves = newWaves

    for inst in sbnk.instruments:
        if isinstance(inst, soundBank.SingleNoteInstrument):
            inst.noteDefinition.waveID = usedWaves.index(
                (inst.noteDefinition.waveArchiveIDID, inst.noteDefinition.waveID))
        elif isinstance(inst, soundBank.RangeInstrument):
            filteredDefinitions = []
            dummyDefinition = inst.noteDefinitions[0]
            for d in inst.noteDefinitions:
                if (d.waveArchiveIDID, d.waveID) in usedWaves:
                    d.waveID = usedWaves.index((d.waveArchiveIDID, d.waveID))
                    filteredDefinitions.append(d)
                else:
                    filteredDefinitions.append(dummyDefinition)
            inst.noteDefinitions = filteredDefinitions
        elif isinstance(inst, soundBank.RegionalInstrument):
            filteredRegions = []
            for reg in inst.regions:
                if (reg.noteDefinition.waveArchiveIDID, reg.noteDefinition.waveID) in usedWaves:
                    reg.noteDefinition.waveID = usedWaves.index(
                        (reg.noteDefinition.waveArchiveIDID, reg.noteDefinition.waveID))
                    filteredRegions.append(
                        soundBank.RegionalInstrument.Region(
                            reg.lastPitch, reg.noteDefinition))
            inst.regions = filteredRegions
            if inst.regions:
                inst.regions[-1].lastPitch = 127 # required


def minifyBySseq(sseq, sbnk, swars=None):
    """
    Minify the given SBNK and optionally SWARs.

    This function is ideal for an SBNK that's used by only one SSEQ.
    This is a common case. Note (todo: figure out how to word this
    better): don't just think, like, "I have three songs using HGSS, so
    this function isn't for me." In most cases, what you actually have
    are three songs using three different copies of HGSS.
    """
    minifyByEvents(sseq.events, sbnk, swars)


def minifyBySseqs(sseqs, sbnk, swars=None):
    """
    Minify the given SBNK and optionally SWARs.

    This function is ideal for an SBNK that's only used by SSEQs. If
    your SBNK is only used by one SSEQ, you can use minifyBySseq()
    instead. That's equivalent to minifyBySseqs([sseq], sbnk, swars).
    """
    def events():
        for sseq in sseqs:
            sseq.parse()
            yield from sseq.events
    minifyByEvents(events(), sbnk, swars)


def durationOf(events,
        initialMonoPolyMode=_MONO):
    """
    Return the sum of all times taken by the given list of events.
    This does NOT take into account any additional time taken by jumps
    or such.
    """

    monoPolyMode = initialMonoPolyMode

    def durationOfEvent(event):
        nonlocal monoPolyMode
        if isinstance(event, soundSequence.RestSequenceEvent):
            return event.duration
        elif (isinstance(event, soundSequence.NoteSequenceEvent)
                and monoPolyMode is _MONO):
            return event.duration
        elif isinstance(event, soundSequence.MonoPolySequenceEvent):
            monoPolyMode = event.value
        return 0

    return sum(map(durationOfEvent, events))


def moveInTime(events, startIndex, time,
        initialMonoPolyMode=_MONO,
        cut=False, append=False):
    """
    Given a list of events and a starting event index, move in time by
    AT MOST the requested amount. Return, as a 3-tuple:
        - the index of the first event at this time (or the length of
          the list if applicable)
        - the amount of time that was moved
        - the mono/poly mode at this time
    Zero-duration events at the end of the time period moved through
    will not be consumed.

    `monoPolyMode` is the initial mono/poly mode. It defaults to `Mono`
    because the DS does. If you're starting at the beginning of a track,
    you shouldn't have to worry about this.

    If `cut` is True, a rest sequence event may be cut into two in order
    to move forward the exact requested amount.

    If `append` is True, a rest sequence event may be appended to a
    track in order to move forward the exact requested amount. (This
    will not occur for looped tracks.)

    Thus, if both of these are False, the events list will be guaranteed
    to be unmodified after the call.

    .. warning::
        Moving backwards in time is currently unsupported, and currently
        throws a ValueError. This may become supported in a future
        release.
    """

    # Special cases for moving backwards in time, and moving zero time
    if time < 0:
        raise ValueError(f'Moving backwards in time is currently unsupported (time={time})')
    elif time == 0:
        return startIndex, 0, initialMonoPolyMode

    elapsedTime = 0
    target = time

    if startIndex > len(events):
        raise ValueError('moveInTime(): startIndex is greater than the'
                         ' list of events!')
    idx = startIndex

    monoPolyMode = initialMonoPolyMode

    time = 0
    while idx < len(events):
        e = events[idx]
        d = durationOf([e], monoPolyMode)
        newElapsedTime = elapsedTime + d

        if isinstance(e, soundSequence.MonoPolySequenceEvent):
            monoPolyMode = e.value

        if newElapsedTime == target:
            # We've hit it exactly! This is where we stop.
            return idx + 1, newElapsedTime, monoPolyMode

        elif newElapsedTime >= target:
            # This event would put us past the target time.
            # Split it in half if it's a rest and we're allowed to;
            # otherwise, don't.
            if isinstance(e, soundSequence.RestSequenceEvent) and cut:
                firstHalfLength = target - elapsedTime
                firstHalf = e
                fullRestLength = firstHalf.duration
                firstHalf.duration = firstHalfLength
                secondHalf = soundSequence.RestSequenceEvent(
                    fullRestLength - firstHalfLength)
                events.insert(idx + 1, secondHalf)
                return idx + 1, target, monoPolyMode

            else:
                return idx, elapsedTime, monoPolyMode

            break

        elapsedTime += d
        idx += 1

    # We made it all the way through without reaching the desired time.
    # Now we extend the list if the caller requested that...
    if append:
        newRest = soundSequence.RestSequenceEvent(target - elapsedTime)
        events.append(newRest)
        elapsedTime = target

    # ... and, whether we extended the list or not, we now return the
    # end of the list.
    return len(events), elapsedTime, monoPolyMode


def moveTo(events, start, end,
        monoPolyMode=_MONO):
    """
    Like moveInTime(), but you move to a specific event. Useful for
    checking the mono/poly mode at that point or the time elapsed
    between two events.
    Returns the elapsed time and the mono/poly mode.

    TODO: do we actually need this now that durationOf() exists?
    """
    raise NotImplementedError


@contextlib.contextmanager
def SimultaneousEventsModifier(events):
    """
    A context manager over a list of events, where you can make changes
    to the list (via the context manager) and the list itself won't
    change until the context is exited. Lets you do nice things like
    events = [a, b, c]
    with SimultaneousEventsModifier(events) as mod:
        events.insert(1, d)
        events.insert(1, e)
        events.insert(1, f)
        events.insert(2, g)
    print(events)
    [a, d, e, f, b, g, c]
    since the indices are always relative to the original list!

    .. warning::
        Don't use this with functions that modify the events list and
        expect you to work with the modified list (e.g. moveInTime with
        cut = True)! Then your indices will be off.

    TODO: probably make this into a legit class instead of this contextmanager
    """
    class LogCreator(list):
        """
        A subclass of list which overrides functions that would modify
        the list, and just writes them to a log instead (.log)
        """
        def __init__(self, other=None):
            if other is None: other = []
            super().__init__(other)
            self.log = {}

        def insert(self, index, item):
            if index not in self.log:
                self.log[index] = {}
            if 'additions' not in self.log[index]:
                self.log[index]['additions'] = []
            self.log[index]['additions'].append(item)

        def __setitem__(self, index, item):
            if index not in self.log:
                self.log[index] = {}
            self.log[index]['replace'] = item

        def __delitem__(self, index):
            if index not in self.log:
                self.log[index] = {}
            self.log[index]['delete'] = True


    logger = LogCreator(events)
    yield logger

    log = logger.log
    for idx in reversed(sorted(log)):
        # If a replacement and a deletion are both requested, just do
        # the replacement
        if 'replace' in log[idx]:
            events[idx] = log[idx]['replace']
        elif log[idx].get('delete', False):
            del events[idx]

        for event in reversed(log[idx].get('additions', [])):
            events.insert(idx, event)


class SSEQMusic:
    """
    An opinionated class that provides a higher-level API around
    SSEQ-based music.

    This allows you to perform some higher-level operations on its
    contents. Unlike the SSEQ class, this assumes some things about the
    SSEQ's structure in order to make it easier to edit.

    .sseq/.sbnk/.swars are NOT guaranteed to be kept up to date until
    just after .save() is called. Also, sbnk and swars are explicitly
    allowed to be None. (Only functions that literally cannot function
    without them, such as Minify, should fail. Also, Minify should be
    able to minify just the SSEQ and leave the SBNK alone if the SSEQ
    and SBNK but not SWAR are present.)
    """

    class Track:
        """
        Class that represents a channel in a SSEQ file.
        """
        def __init__(self, events):
            self.events = list(events)
            if self.events:
                if isinstance(self.events[-1], soundSequence.EndTrackSequenceEvent):
                    self.events.pop()


        @property
        def looped(self):
            return any(isinstance(e, soundSequence.JumpSequenceEvent)
                for e in self.events)


        def loop(self, start, end, *, clearTrailing=True):
            """
            Loop the track.
            `start` and `end` are integers, in the same units used for
            durations in the SSEQ.
            If `clearTrailing` is set, all events after the end of the
            loop will be deleted.
            """
            if self.looped:
                raise RuntimeError("Can't loop a track that's already"
                                   ' looped')

            loopStartIdx, actualStartTime, _ = moveInTime(
                self.events, 0, start, cut=True, append=True)

            if actualStartTime != start:
                raise RuntimeError(f'Unable to start the loop at {start}'
                                   f' (only able to start it at'
                                   f' {actualStartTime})')

            loopEndIdx, actualEndTime, _ = moveInTime(
                self.events, 0, end, cut=True, append=True)

            if actualEndTime != end:
                raise RuntimeError(f'Unable to end the loop at {end}'
                                   f' (only able to end it at'
                                   f' {actualEndTime})')

            jumpTarget = self.events[loopStartIdx]
            jump = soundSequence.JumpSequenceEvent(jumpTarget)
            self.events.insert(loopEndIdx, jump)

            if clearTrailing:
                self.events = self.events[:loopEndIdx + 1]


        def _modifyNoteVelocities(self, func, *, clamp=True):
            for e in self.events:
                if not isinstance(e, soundSequence.NoteSequenceEvent):
                    continue
                newVelocity = int(func(e.velocity))
                if not (0 <= newVelocity <= 127):
                    if clamp:
                        newVelocity = min(max(newVelocity, 0), 127)
                    else:
                        raise ValueError('Attempted to set note velocity to'
                                        f' {newVelocity} (not in range'
                                         ' 0..127)')
                e.velocity = newVelocity


        def addToNoteVelocities(self, amount, *, clamp=True):
            def adder(velocity):
                return velocity + amount
            self._modifyNoteVelocities(adder, clamp=clamp)


        def multiplyNoteVelocitiesBy(self, factor, *, clamp=True):
            def multiplier(velocity):
                return velocity * factor
            self._modifyNoteVelocities(multiplier, clamp=clamp)


        # Properties that add/remove events at the beginning of the list:
        # initialTempo, initialMonoPoly, initialChannelVolume, initialInstrument, etc

        def _findControlEventAtBeginning(self, type):
            for e in self.events:
                if isinstance(e, type):
                    return e
                elif (isinstance(e, soundSequence.NoteSequenceEvent)
                        or isinstance(e, soundSequence.RestSequenceEvent)):
                    break

        def _handleInitialValueGet(self, type, *, isInstrumentSwitch=False):
            event = self._findControlEventAtBeginning(type)
            if event is None: return None
            if isInstrumentSwitch:
                return event.bankID, event.instrumentID
            else:
                return event.value

        def _handleInitialValueSet(self, type, value, *, isInstrumentSwitch=False):

            event = self._findControlEventAtBeginning(type)

            if event is None and value is None:
                # No event exists yet and we're supposed to delete it.
                # Do nothing.
                pass

            elif event is None:
                # No event exists yet and we're supposed to give it a
                # new value. Make a new event and add it.
                if isInstrumentSwitch:
                    event = type(value[0], value[1])
                else:
                    event = type(value)
                self.events.insert(0, event)

            elif value is None:
                # An event exists and we're supposed to delete it.
                self.events.remove(event)

            else:
                # An event exists and we're supposed to give it a new
                # value.
                if isInstrumentSwitch:
                    event.bankID = value[0]
                    event.instrumentID = value[1]
                else:
                    event.value = value

        @property
        def initialInstrument(self):
            return self._handleInitialValueGet(
                soundSequence.InstrumentSwitchSequenceEvent,
                isInstrumentSwitch=True)
        @initialInstrument.setter
        def initialInstrument(self, value):
            return self._handleInitialValueSet(
                soundSequence.InstrumentSwitchSequenceEvent,
                value,
                isInstrumentSwitch=True)

        @property
        def initialPan(self):
            return self._handleInitialValueGet(soundSequence.PanSequenceEvent)
        @initialPan.setter
        def initialPan(self, value):
            return self._handleInitialValueSet(soundSequence.PanSequenceEvent,
                                               value)

        @property
        def initialVolume(self):
            return self._handleInitialValueGet(
                soundSequence.TrackVolumeSequenceEvent)
        @initialVolume.setter
        def initialVolume(self, value):
            return self._handleInitialValueSet(
                soundSequence.TrackVolumeSequenceEvent, value)

        @property
        def initialTranspose(self):
            return self._handleInitialValueGet(
                soundSequence.TransposeSequenceEvent)
        @initialTranspose.setter
        def initialTranspose(self, value):
            return self._handleInitialValueSet(
                soundSequence.TransposeSequenceEvent, value)

        @property
        def initialPriority(self):
            return self._handleInitialValueGet(
                soundSequence.TrackPrioritySequenceEvent)
        @initialPriority.setter
        def initialPriority(self, value):
            return self._handleInitialValueSet(
                soundSequence.TrackPrioritySequenceEvent, value)

        @property
        def initialMonoPoly(self):
            return self._handleInitialValueGet(
                soundSequence.MonoPolySequenceEvent)
        @initialMonoPoly.setter
        def initialMonoPoly(self, value):
            return self._handleInitialValueSet(
                soundSequence.MonoPolySequenceEvent, value)

        @property
        def initialAttackRate(self):
            return self._handleInitialValueGet(
                soundSequence.AttackRateSequenceEvent)
        @initialAttackRate.setter
        def initialAttackRate(self, value):
            return self._handleInitialValueSet(
                soundSequence.AttackRateSequenceEvent, value)

        @property
        def initialDecayRate(self):
            return self._handleInitialValueGet(
                soundSequence.DecayRateSequenceEvent)
        @initialDecayRate.setter
        def initialDecayRate(self, value):
            return self._handleInitialValueSet(
                soundSequence.DecayRateSequenceEvent, value)

        @property
        def initialSustainRate(self):
            return self._handleInitialValueGet(
                soundSequence.SustainRateSequenceEvent)
        @initialSustainRate.setter
        def initialSustainRate(self, value):
            return self._handleInitialValueSet(
                soundSequence.SustainRateSequenceEvent, value)

        @property
        def initialReleaseRate(self):
            return self._handleInitialValueGet(
                soundSequence.ReleaseRateSequenceEvent)
        @initialReleaseRate.setter
        def initialReleaseRate(self, value):
            return self._handleInitialValueSet(
                soundSequence.ReleaseRateSequenceEvent, value)

        @property
        def initialTempo(self):
            return self._handleInitialValueGet(
                soundSequence.TempoSequenceEvent)
        @initialTempo.setter
        def initialTempo(self, value):
            return self._handleInitialValueSet(
                soundSequence.TempoSequenceEvent, value)


        def __str__(self):
            linesList = ['<track']
            linesList.append(soundSequence.printSequenceEventList(
                self.events, {}, ' ' * 2))
            linesList.append('>')
            return '\n'.join(linesList)


        def __repr__(self):
            return f'{type(self).__name__}({self.events!r})'


    def __init__(self, sseq, sbnk=None, swars=None):
        self.sseq = sseq
        self.sbnk = sbnk
        self.swars = swars
        if not _common.isIterable(self.swars):
            raise TypeError('SWAR list is not iterable (did you'
                ' accidentally pass a SWAR to the constructor instead'
                ' of a list of SWARs?)')

        # Parse the SSEQ if it's not already
        if not sseq.parsed:
            sseq.parse()

        # Make a dictionary of tracks
        # Each track's events are considered to end whenever another
        # track begins.
        self.tracks = {}
        if isinstance(sseq.events[0],
                soundSequence.DefineTracksSequenceEvent):

            # Find events that begin tracks (so that we know where to
            # end tracks)
            # (the beginning of track 0 is omitted from this list, but
            # that's OK)
            trackStarts = []
            i = 1
            while isinstance(sseq.events[i],
                    soundSequence.BeginTrackSequenceEvent):
                trackStarts.append(sseq.events[i].firstEvent)
                i += 1

            # Track 0 doesn't have a BeginTrack event
            if 0 in sseq.events[0].trackNumbers:
                # Find where the BeginTrack events end
                startIdx = 1
                while isinstance(sseq.events[startIdx],
                        soundSequence.BeginTrackSequenceEvent):
                    startIdx += 1
                endIdx = startIdx + 1
                while (endIdx < len(sseq.events)
                        and sseq.events[endIdx] not in trackStarts):
                    endIdx += 1

                trackEvents = sseq.events[startIdx : endIdx]
                self.tracks[0] = self.Track(trackEvents)

            # Create the Track objects
            i = 1
            while isinstance(sseq.events[i],
                    soundSequence.BeginTrackSequenceEvent):
                e = sseq.events[i]
                startIdx = sseq.events.index(e.firstEvent)
                endIdx = startIdx + 1
                while (endIdx < len(sseq.events)
                        and sseq.events[endIdx] not in trackStarts):
                    endIdx += 1

                trackEvents = sseq.events[startIdx : endIdx]
                self.tracks[e.trackNumber] = self.Track(trackEvents)
                i += 1

        else:
            self.tracks[0] = self.Track(sseq.events)


    def loop(self, start, end, *, clearTrailing=True):
        """
        Loop all tracks in the SSEQ.
        `start` and `end` are integers, in the same units used for
        durations in the SSEQ.
        `clearTrailing` has the same meaning as in Track.loop().
        """
        for track in self.tracks.values():
            track.loop(start, end, clearTrailing=clearTrailing)


    def minify(self):
        """
        Minify the song (SSEQ, optionally SBNK, optionally SWAR)
        The SBNK and SWAR will be modified, so be forewarned
        (this may cause unintended side-effects if you're reusing the
        same bank/swar in multiple places)
        Also, don't use this if multiple songs use the same SBNK.
        Use minifyBySseqs() instead in that case, after calling save()
        on this object.
        """
        if self.sbnk is None:
            # There's nothing to minify if there's no SBNK
            return

        def events():
            for track in self.tracks.values():
                yield from track.events
        minifyByEvents(events(), self.sbnk, self.swars)


    def collapseTrackIDs(self):
        """
        If the current track IDs are like
        0, 1, 2, 4, 5, 8, 9, 10
        , this function renumbers them to the saner
        0, 1, 2, 3, 4, 5, 6, 7
        while preserving their order.
        """
        newTracks = {}
        for i, id in enumerate(sorted(self.tracks.keys())):
            newTracks[i] = self.tracks[id]
        self.tracks = newTracks


    def save(self):
        """
        Update self.sseq / self.sbnk / self.swars to reflect changes
        made in self.tracks, and return them. You can safely use those
        properties after calling this function, until you start making
        changes again.
        """
        # Rebuild sseq.events
        if len(self.tracks) == 1 and 0 in self.tracks:
            # There's only one track and it's track 0. Don't bother
            # defining tracks and stuff.
            self.sseq.events = list(self.tracks[0].events)
            if not (isinstance(self.sseq.events[-1],
                               soundSequence.EndTrackSequenceEvent)
                    or isinstance(self.sseq.events[-1],
                                  soundSequence.JumpSequenceEvent)):
                self.sseq.events.append(soundSequence.EndTrackSequenceEvent())

        else:
            beginning = []
            contents = []

            dfse = soundSequence.DefineTracksSequenceEvent(set(self.tracks))
            beginning.append(dfse)

            for trackNum in sorted(self.tracks):
                track = self.tracks[trackNum]
                if not track.events:
                    # Um.
                    continue

                if trackNum != 0:
                    beginning.append(
                        soundSequence.BeginTrackSequenceEvent(
                            trackNum, track.events[0]))
                contents.extend(track.events)
                if not (isinstance(contents[-1],
                                   soundSequence.EndTrackSequenceEvent)
                        or isinstance(contents[-1],
                                      soundSequence.JumpSequenceEvent)):
                    contents.append(soundSequence.EndTrackSequenceEvent())

            self.sseq.events = beginning + contents

        return self.sseq, self.sbnk, self.swars


    def __str__(self):
        trackNums = sorted(self.tracks)
        trackNumStrs = [str(x) for x in trackNums]
        return f'<sseq music [tracks: {", ".join(trackNumStrs)}]>'


    def __repr__(self):
        return f'{type(self).__name__}({self.sseq!r})'
