def _cmd_autotrack(self):
        """Start Autotracking"""
        # first get pid, see the 32-bit solution

        PROCNAME = "KINGDOM HEARTS II FINAL MIX"


        try:
           kh2=pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
        except:
            self.output("Game is not Open")
        #Save = 0x09A70B0
        ##pid = None
        ##
        ##
        ##for proc in psutil.process_iter():
        ##    if PROCNAME in proc.name():
        ##       pid = proc.pid
        ##       base=int(proc.memory_maps(False)[0].addr,0)
        ##
        #kh2=pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
        #
        #yourmom=kh2.base_address + Save+0x23DF
        ##if kh2.read_bytes(yourmom,1)&0x04:
        ##	print("your mom")
        ##else:
        ##	print("")
        #
        #chestvalue=int.from_bytes(kh2.read_bytes(yourmom,1), "big")
        ##check if chest is already opened 
        ##chestvalue is total amount of chests opened. 
        #print(kh2.write_bytes(yourmom,(chestvalue|0x1<<2).to_bytes(1,'big'),1))
        #
        #
        #
        ##opens the chest at value 2 and keeps all the other chests the same
        #kh2.write_bytes(yourmom,(chestvalue|0x1<<2).to_bytes(1,'big'),1)

    #def _cmd_gb(self):
    #    """Check Gameboy Connection State"""
    #    if isinstance(self.ctx, KH2Context):
    #        logger.info("debussy")