import pathlib
import subprocess
import tempfile

import ndspy.color
import ndspy.texture


def paletteReduceImage(img, numColors):
    """
    Given an image and a desired maximum number of colors,
    palette-reduce the image using libimagequant.
    Return a list of ints containing indices, and a list of (r, g, b, a)
    palette colors.
    """
    with tempfile.TemporaryDirectory() as tempdir:
        temppath = pathlib.Path(tempdir)

        data = bytearray(img.width * img.height * 4)
        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = img.getpixel((x, y))
                data[(y * img.width + x) * 4 + 0] = r
                data[(y * img.width + x) * 4 + 1] = g
                data[(y * img.width + x) * 4 + 2] = b
                data[(y * img.width + x) * 4 + 3] = a

        (temppath / 'input.bin').write_bytes(data)

        here = pathlib.Path(__file__).resolve().parent
        liqPath = here / 'libimagequant-wrapper/libimagequant-wrapper'

        subprocess.run([str(liqPath),
                        str(temppath / 'input.bin'),
                        str(temppath / 'output_tex.bin'),
                        str(temppath / 'output_pal.bin'),
                        str(img.width),
                        str(img.height),
                        str(numColors)])

        indicesData = (temppath / 'output_tex.bin').read_bytes()
        palData = (temppath / 'output_pal.bin').read_bytes()

        indices = list(indicesData)

        pal = []
        for i in range(len(palData) // 4):
            pal.append(tuple(palData[i * 4: i * 4 + 4]))

        return indices, pal


def encodeImage(img, format):
    """
    Given a PIL.Image and a TextureFormat, return:
    - texture data (main)
    - texture data (sub) (may be None)
    - palette (as a list of color values) (may be None)
    """
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    fxn = {
        ndspy.texture.TextureFormat.TRANSLUCENT_A3I5: encodeImage_A3I5,
        ndspy.texture.TextureFormat.PALETTED_2BPP: encodeImage_Paletted_2BPP,
        ndspy.texture.TextureFormat.PALETTED_4BPP: encodeImage_Paletted_4BPP,
        ndspy.texture.TextureFormat.PALETTED_8BPP: encodeImage_Paletted_8BPP,
        ndspy.texture.TextureFormat.TEXELED_4X4: encodeImage_Texeled_4x4,
        ndspy.texture.TextureFormat.TRANSLUCENT_A5I3: encodeImage_A5I3,
        ndspy.texture.TextureFormat.DIRECT_16_BIT: encodeImage_Direct_16_Bit,
    }.get(format)

    if fxn is None:
        raise ValueError(f'Unsupported texture format: {format}')
    return fxn(img)


def encodeImage_A3I5(img):
    """
    Encode the given image in the A3I5 format.
    """
    indices, palette = paletteReduceImage(img, 32)

    tex = bytearray()
    for idx in indices:
        color = palette[idx]
        a = color[3]
        value = idx | (a & 0xE0)
        tex.append(value)

    return tex, None, encodePalette(palette)


def encodeImage_Paletted_2BPP(img):
    """
    Encode the given image in the Paletted 2BPP format.
    """
    indices, palette = paletteReduceImage(img, 4)

    tex = bytearray()
    for i in range(len(indices) // 4):
        v1 = indices[i * 4 + 0]
        v2 = indices[i * 4 + 1]
        v3 = indices[i * 4 + 2]
        v4 = indices[i * 4 + 3]
        v = v4 << 6 | v3 << 4 | v2 << 2 | v1
        tex.append(v)

    return tex, None, encodePalette(palette)


def encodeImage_Paletted_4BPP(img):
    """
    Encode the given image in the Paletted 4BPP format.
    """
    indices, palette = paletteReduceImage(img, 16)

    tex = bytearray()
    for i in range(len(indices) // 2):
        v1 = indices[i * 2 + 0]
        v2 = indices[i * 2 + 1]
        v = v2 << 4 | v1
        tex.append(v)

    return tex, None, encodePalette(palette)


def encodeImage_Paletted_8BPP(img):
    """
    Encode the given image in the Paletted 8BPP format.
    """
    indices, palette = paletteReduceImage(img, 256)
    return bytes(indices), None, encodePalette(palette)



class _Mode5Texel:
    """
    A texel in mode 5.
    """
    def __init__(self, img):

        # Simplify alpha channel to 1 bit
        haveAlpha = False
        origColors = self.origColors = []
        for y in range(4):
            for x in range(4):
                r, g, b, a = img.getpixel((x, y))
                if a < 128:
                    haveAlpha = True
                    r = g = b = newA = 0
                else:
                    newA = 255
                if newA != a:
                    img.putpixel((x, y), (r, g, b, newA))
                origColors.append((r, g, b, newA))

        # And *now* actually reduce the image
        indices, palette = paletteReduceImage(img, 4)
        if len(palette) % 2: palette.append((0, 0, 0, 0))
        self.palette = palette

        # self.scores = {}

        # Only modes 0 and 1 are allowed if we have alpha
        if haveAlpha:
            self.renderings = {0: None, 1: None}
        else:
            self.renderings = {0: None, 1: None, 2: None, 3: None}

        self.rerenderForModes()

    def rerenderForModes(self):
        """
        Rerender ourselves for all currently available modes
        """
        self.scores.clear()
        which = set(self.renderings.keys())
        self.renderings.clear()

        if 0 in which:
            color0 = None # todo: fill in
            self.renderings[0] = None # todo: fill in
        self.renderings[2] = self.indices

        self.indices, self.palette = indices, palette

    def encode(self):
        """
        Encode ourselves as best we currently can
        """
        interpMode = 2

        iter_ = iter(self.indices)

        data = bytearray()
        for suby in range(4):
            value1 = 0
            for subx in range(4):
                value1 >>= 2
                value1 |= next(iter_) << 6
            data.append(value1)

        return interpMode, data


def encodeImage_Texeled_4x4(img):
    """
    Encode the given image in the Texeled 4x4 format.
    """
    if img.width % 4 or img.height % 4:
        raise ValueError(f'Cannot encode {img.width}x{img.height} image as'
            ' texeled 4x4 (width and height must be multiples of 4)!')

    # Get texels
    texels = []
    palettes = []
    for y in range(0, img.height, 4):
        for x in range(0, img.width, 4):
            tx = _Mode5Texel(img.crop((x, y, x + 4, y + 4)))
            texels.append(tx)
            palettes.append(tx.palette)

    def generateMasterPalette(palettes):
        """
        Generate a master palette from the given palettes.
        """
        mp = []
        mpOffsets = {}
        offsets = []
        for p in palettes:
            if id(p) in mpOffsets:
                offs = mpOffsets[id(p)]
            else:
                mpOffsets[id(p)] = offs = len(mp)
                mp.append(p)
            offsets.append(offs)

        return mp, offsets

    # Shrink
    ...

    # Generate the master palette
    masterPalette, masterPaletteOffsets = generateMasterPalette(palettes)

    # Save output
    data1 = bytearray()
    data2 = bytearray()
    for tx, paletteOffset in zip(texels, masterPaletteOffsets):
        interpMode, data = tx.encode()
        interpMode = 2

        data1.extend(data)

        value2 = interpMode << 14 | (paletteOffset // 2)
        data2.append(value2 & 0xFF)
        data2.append(value2 >> 8)

    return bytes(data1), bytes(data2), encodePalette(masterPalette)


    # Each 4x4 texel has a palette offset that is a multiple of 2
    # And an interpolation mode. color0
    # Mode 0: 3 direct colors, and transparent
    #     Pixel value 0: color0
    #     Pixel value 1: color1
    #     Pixel value 2: color2
    #     Pixel value 3: transparent
    # Mode 1: 2 direct colors, their average, and transparent
    #     Pixel value 0: color0
    #     Pixel value 1: color1
    #     Pixel value 2: (color0 + color1) / 2
    #     Pixel value 3: transparent
    # Mode 2: 4 direct colors
    #     Pixel value 0: color0
    #     Pixel value 1: color1
    #     Pixel value 2: color2
    #     Pixel value 3: color3
    # Mode 3: 2 direct colors and 2 weighted averages
    #     Pixel value 0: color0
    #     Pixel value 1: color1
    #     Pixel value 2: (color0 * 5 + color1 * 3) / 8
    #     Pixel value 3: (color0 * 3 + color1 * 5) / 8

    # Every mode uses color0 and color1. Mode 0 also uses color2, and mode 2 uses colors 0 through 3

    # OK. Well, we can iteratively figure out if the best* course of action is to
    # merge two palettes or to shrink a palette into using one of the compressed texel modes.
    # At each step, we can try putting the palettes together to see how small it ends up,
    # and use that as the stopping condition.

    # *"Best" is a function of how much memory we'll save AND how much it hurts the image.
    # The latter is tricky to calculate.



    raise NotImplementedError

    # ImageTexeler imageTexeler = new ImageTexeler(bitmap, (int)this.nsbtx.PalInfo.infoBlock.PalInfo[(int)argument[1]].pal.Length / 4, ref backgroundWorker);

    # this.nsbtx.TexInfo.infoBlock.TexInfo[(int)argument[0]].Image = imageTexeler.texdata;
    # this.nsbtx.TexInfo.infoBlock.TexInfo[(int)argument[0]].format = 5;
    # this.nsbtx.TexInfo.infoBlock.TexInfo[(int)argument[0]].spData = imageTexeler.f5data;
    # this.nsbtx.TexInfo.infoBlock.TexInfo[(int)argument[0]].height = (ushort)bitmap.Height;
    # this.nsbtx.TexInfo.infoBlock.TexInfo[(int)argument[0]].width = (ushort)bitmap.Width;
    # this.nsbtx.TexInfo.infoBlock.TexInfo[(int)argument[0]].color0 = 0;
    # this.nsbtx.PalInfo.infoBlock.PalInfo[(int)argument[1]].pal = imageTexeler.finalPalette;


def encodeImage_A5I3(img):
    """
    Encode the given image in the A5I3 format.
    """
    indices, palette = paletteReduceImage(img, 8)

    tex = bytearray()
    for idx in indices:
        color = palette[idx]
        a = color[3]
        value = idx | (a & 0xF8)
        tex.append(value)

    return tex, None, encodePalette(palette)


def encodeImage_Direct_16_Bit(img):
    """
    Encode the given image in the Direct 16-bit format.
    """
    data = bytearray(img.width * img.height * 2)
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = img.getpixel((x, y))
            val = ndspy.color.pack255(r, g, b, 255 - a)
            data[(x + y * img.width) * 2] = val & 0xFF
            data[(x + y * img.width) * 2 + 1] = val >> 8

    return data, None, None


def encodePalette(palette):
    """
    Given a list of (r, g, b, a) colors, return a list of packed colors,
    padded to a multiple of 4.
    """
    palPacked = []
    for r, g, b, a in palette:
        palPacked.append(ndspy.color.pack255(r, g, b, a))
    while len(palPacked) % 4: palPacked.append(0)
    return palPacked



        # private void CreateTexture(int type)
        # {
        #     int width;
        #     int height;
        #     Bitmap bitmap;
        #     Graphics graphic;
        #     int i;
        #     int j;
        #     int num;
        #     bool flag;
        #     if ((this.openFileDialog1.ShowDialog() != System.Windows.Forms.DialogResult.OK ? false : this.openFileDialog1.FileName.Length > 0))
        #     {
        #         Bitmap bitmap1 = new Bitmap(Image.FromFile(this.openFileDialog1.FileName));
        #         int num1 = 8;
        #         int num2 = 8;
        #         int num3 = 0;
        #         int num4 = 0;
        #         while (num1 < bitmap1.Width)
        #         {
        #             num1 *= 2;
        #             num3++;
        #         }
        #         while (num2 < bitmap1.Height)
        #         {
        #             num2 *= 2;
        #             num4++;
        #         }
        #         if ((type != 5 || num2 <= 256 ? num1 > 256 : true))
        #         {
        #             num2 = 256;
        #             num1 = 256;
        #         }
        #         if ((num1 < bitmap1.Width ? false : num2 >= bitmap1.Height))
        #         {
        #             bitmap = new Bitmap(num1, num2);
        #             graphic = Graphics.FromImage(bitmap);
        #             try
        #             {
        #                 graphic.SmoothingMode = SmoothingMode.AntiAlias;
        #                 graphic.InterpolationMode = InterpolationMode.HighQualityBicubic;
        #                 graphic.PixelOffsetMode = PixelOffsetMode.HighQuality;
        #                 graphic.DrawImage(bitmap1, new Rectangle(0, 0, bitmap1.Width, bitmap1.Height));
        #             }
        #             finally
        #             {
        #                 if (graphic != null)
        #                 {
        #                     ((IDisposable)graphic).Dispose();
        #                 }
        #             }
        #             bitmap1 = bitmap;
        #         }
        #         else
        #         {
        #             if (bitmap1.Height <= bitmap1.Width)
        #             {
        #                 width = num1;
        #                 height = bitmap1.Height * num2 / bitmap1.Width;
        #             }
        #             else
        #             {
        #                 height = num2;
        #                 width = bitmap1.Width * num1 / bitmap1.Height;
        #             }
        #             MessageBox.Show("The picture isn't a power of 2. It will be resized. It can be that there is a transparent border around the picture.");
        #             bitmap = new Bitmap(num1, num2);
        #             graphic = Graphics.FromImage(bitmap);
        #             try
        #             {
        #                 graphic.SmoothingMode = SmoothingMode.AntiAlias;
        #                 graphic.InterpolationMode = InterpolationMode.HighQualityBicubic;
        #                 graphic.PixelOffsetMode = PixelOffsetMode.HighQuality;
        #                 graphic.DrawImage(bitmap1, new Rectangle(0, 0, width, height));
        #             }
        #             finally
        #             {
        #                 if (graphic != null)
        #                 {
        #                     ((IDisposable)graphic).Dispose();
        #                 }
        #             }
        #             bitmap1 = bitmap;
        #         }
        #         if (type == 5)
        #         {
        #             BackgroundWorker backgroundWorker = new BackgroundWorker()
        #             {
        #                 WorkerReportsProgress = true,
        #                 WorkerSupportsCancellation = true
        #             };
        #             backgroundWorker.DoWork += new DoWorkEventHandler(this.tex4x4);
        #             backgroundWorker.ProgressChanged += new ProgressChangedEventHandler(this.bw_ProgressChanged);
        #             backgroundWorker.RunWorkerCompleted += new RunWorkerCompletedEventHandler(this.bw_RunWorkerCompleted);
        #             object[] selectedIndex = new object[] { this.listBox1.SelectedIndex, this.listBox2.SelectedIndex, bitmap1 };
        #             backgroundWorker.RunWorkerAsync(selectedIndex);
        #             this.bwr = backgroundWorker;
        #             this.toolStripDropDownButton1.Enabled = true;
        #             this.listBox1.SetSelected(this.listBox1.SelectedIndex, true);
        #         }
        #         else
        #         {
        #             Color[] fuchsia = new Color[0];
        #             if (!(type == 4 || type == 3 ? false : type != 2))
        #             {
        #                 bool flag1 = false;
        #                 for (i = 0; i < bitmap1.Width; i++)
        #                 {
        #                     for (j = 0; j < bitmap1.Height; j++)
        #                     {
        #                         if (bitmap1.GetPixel(i, j).A == 0)
        #                         {
        #                             flag1 = true;
        #                         }
        #                     }
        #                 }
        #                 num = type;
        #                 switch (num)
        #                 {
        #                     case 2:
        #                     {
        #                         fuchsia = ImageIndexer.createPaletteForImage(bitmap1, 4, flag1);
        #                         break;
        #                     }
        #                     case 3:
        #                     {
        #                         fuchsia = ImageIndexer.createPaletteForImage(bitmap1, 16, flag1);
        #                         break;
        #                     }
        #                     case 4:
        #                     {
        #                         fuchsia = ImageIndexer.createPaletteForImage(bitmap1, 256, flag1);
        #                         break;
        #                     }
        #                 }
        #             }
        #             else if (type != 7)
        #             {
        #                 num = type;
        #                 if (num == 1)
        #                 {
        #                     fuchsia = ImageIndexer.createPaletteForImage(bitmap1, 32, false);
        #                 }
        #                 else if (num == 6)
        #                 {
        #                     fuchsia = ImageIndexer.createPaletteForImage(bitmap1, 8, false);
        #                 }
        #             }
        #             List<byte> nums = new List<byte>();
        #             num = type;
        #             switch (num)
        #             {
        #                 case 1:
        #                 case 4:
        #                 case 6:
        #                 {
        #                     nums.AddRange(new byte[bitmap1.Width * bitmap1.Height]);
        #                     break;
        #                 }
        #                 case 2:
        #                 case 5:
        #                 {
        #                     nums.AddRange(new byte[bitmap1.Width * bitmap1.Height / 4]);
        #                     break;
        #                 }
        #                 case 3:
        #                 {
        #                     nums.AddRange(new byte[bitmap1.Width * bitmap1.Height / 2]);
        #                     break;
        #                 }
        #                 case 7:
        #                 {
        #                     nums.AddRange(new byte[bitmap1.Width * bitmap1.Height * 2]);
        #                     break;
        #                 }
        #             }
        #             bool flag2 = false;
        #             for (i = 0; i < bitmap1.Width; i++)
        #             {
        #                 for (j = 0; j < bitmap1.Height; j++)
        #                 {
        #                     Color pixel = bitmap1.GetPixel(i, j);
        #                     if (pixel.A == 0)
        #                     {
        #                         flag2 = true;
        #                     }
        #                     int argb = pixel.ToArgb();
        #                     if (type != 7)
        #                     {
        #                         argb = this.getClosestColor(pixel, fuchsia);
        #                     }
        #                     nums = this.setPixel(i, j, argb, bitmap1.Width, bitmap1.Height, type, nums, (int)pixel.A);
        #                 }
        #             }
        #             byte[] array = nums.ToArray();
        #             if (!flag2 || !fuchsia.Contains<Color>(Color.Transparent))
        #             {
        #                 flag = true;
        #             }
        #             else
        #             {
        #                 flag = (type == 4 || type == 3 ? false : type != 2);
        #             }
        #             if (flag)
        #             {
        #                 this.nsbtx.TexInfo.infoBlock.TexInfo[this.listBox1.SelectedIndex].color0 = 0;
        #             }
        #             else
        #             {
        #                 if (fuchsia.Contains<Color>(Color.Fuchsia))
        #                 {
        #                     fuchsia[0] = Color.Fuchsia;
        #                 }
        #                 else
        #                 {
        #                     fuchsia[0] = Color.Fuchsia;
        #                 }
        #                 this.nsbtx.TexInfo.infoBlock.TexInfo[this.listBox1.SelectedIndex].color0 = 1;
        #             }
        #             this.nsbtx.TexInfo.infoBlock.TexInfo[this.listBox1.SelectedIndex].Image = array;
        #             this.nsbtx.TexInfo.infoBlock.TexInfo[this.listBox1.SelectedIndex].height = (ushort)bitmap1.Height;
        #             this.nsbtx.TexInfo.infoBlock.TexInfo[this.listBox1.SelectedIndex].width = (ushort)bitmap1.Width;
        #             this.nsbtx.TexInfo.infoBlock.TexInfo[this.listBox1.SelectedIndex].spData = new byte[0];
        #             this.nsbtx.TexInfo.infoBlock.TexInfo[this.listBox1.SelectedIndex].format = (byte)type;
        #             if (type != 7)
        #             {
        #                 this.nsbtx.PalInfo.infoBlock.PalInfo[this.listBox2.SelectedIndex].pal = fuchsia;
        #             }
        #             this.listBox1.SetSelected(this.listBox1.SelectedIndex, true);
        #         }
        #     }
        # }