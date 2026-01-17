

class ImageTexeler:
    img = None
    palettes = None
    paletteCounts = None
    paletteNumbers = None
    paletteDiffs = None
    f5data = None
    texdata = None
    finalPalette = None

    def __init__(img, paletteMaxNum, bw):

        self.img = img

        width = img.width / 4
        height = img.height / 4

        self.palettes = []
        self.paletteCounts = []
        self.paletteNumbers = []
        for y in range(height):
            self.paletteNumbers.append([0] * width)
        self.paletteDiffs = []
        for y in range(width * height):
            self.paletteDiffs.append([0] * (width * height))

        num1 = 18 / (width * height)
        num2 = 10
        num3 = num4 = 0
        num5 = 100 / (width * height)
        L = 0

        while True:
            if L < width:
                m = 0
                while m < height:
                    bitmap1 = img.crop(L * 4, m * 4, L * 4 + 4, m * 4 + 4)

                    flag = False
                    for i in range(4):
                        num6 = 0
                        while num6 < 4:
                            if bitmap1.getpixel((i, num6))[3] >= 128:
                                num6 += 1
                            else:
                                flag = True
                                break

                    _, colors = paletteReduceImage(bitmap1, 4)
                    self.transparentToTheEnd(colors)

                    num7 = self.contains()

                    Label1:
                        List<Color> colors = new List<Color>();
                        colors.AddRange(ImageIndexer.createPaletteForImage(bitmap1, 4, flag));
                        Color[] array = colors.ToArray();
                        this.transparentToTheEnd(array);
                        int num7 = this.contains(this.palettes.ToArray(), array);
                        if (num7 == -1)
                        {
                            this.palettes.Add(array);
                            this.paletteNumbers[l, m] = this.palettes.Count - 1;
                            this.paletteCounts.Add(1);
                            this.calcPaletteDiffs(this.palettes.Count - 1);
                        }
                        else
                        {
                            this.paletteNumbers[l, m] = num7;
                        }
                        num3++;
                        num2 += num1;
                        bw.ReportProgress((int)num2, string.Concat("Generating Picture ", num4.ToString("000"), "%"));
                        num4 += num5;
                        if (!bw.CancellationPending)
                        {
                            m++;
                        }
                        else
                        {
                            bw.ReportProgress(0, "Canceled");
                            return;
                        }
                    }
                    l++;
                }
                else
                {
                    num4 = 0;
                    num5 = 100 / ((double)this.countUsedPalettes() - 1024);
                    num1 = 74 / ((double)this.countUsedPalettes() - 1024);
                    double num8 = 0;
                    while (this.countUsedPalettes() > 1024)
                    {
                        num8 += 1;
                        int num9 = -1;
                        int num10 = -1;
                        float single = float.MaxValue;
                        for (j = 0; j < this.palettes.Count; j++)
                        {
                            if (this.paletteCounts[j] != 0)
                            {
                                for (int k = 0; k < this.palettes.Count; k++)
                                {
                                    if (j != k)
                                    {
                                        if (this.paletteCounts[k] != 0)
                                        {
                                            if (this.paletteDiffs[j, k] < single)
                                            {
                                                single = this.paletteDiffs[j, k];
                                                num9 = k;
                                                num10 = j;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        this.palettes[num9] = this.palMerge(this.palettes[num9], this.palettes[num10]);
                        this.calcPaletteDiffs(num9);
                        List<int> item = this.paletteCounts;
                        List<int> nums = item;
                        int num11 = num9;
                        int num12 = num11;
                        item[num11] = nums[num12] + this.paletteCounts[num10];
                        this.paletteCounts[num10] = 0;
                        for (l = 0; l < width; l++)
                        {
                            for (m = 0; m < height; m++)
                            {
                                if (this.paletteNumbers[l, m] == num10)
                                {
                                    this.paletteNumbers[l, m] = num9;
                                }
                            }
                        }
                        num2 += num1;
                        num4 += num5;
                        bw.ReportProgress((int)num2, string.Concat("Generating Palette ", num4.ToString("000"), "%"));
                        if (bw.CancellationPending)
                        {
                            bw.ReportProgress(0, "Canceled");
                            return;
                        }
                    }
                    int num13 = 0;
                    this.finalPalette = new Color[this.countUsedPalettes() * 4];
                    int[] numArray = new int[this.palettes.Count];
                    for (j = 0; j < this.palettes.Count; j++)
                    {
                        if (this.paletteCounts[j] != 0)
                        {
                            this.transparentToTheEnd(this.palettes[j]);
                            numArray[j] = num13;
                            Array.Copy(this.palettes[j], 0, this.finalPalette, num13 * 4, 4);
                            num13++;
                        }
                    }
                    ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                    ByteArrayOutputStream byteArrayOutputStream1 = new ByteArrayOutputStream();
                    for (m = 0; m < height; m++)
                    {
                        for (l = 0; l < width; l++)
                        {
                            bool flag1 = false;
                            for (n = 0; n < 4; n++)
                            {
                                for (o = 0; o < 4; o++)
                                {
                                    pixel = img.GetPixel(l * 4 + o, m * 4 + n);
                                    if (pixel.A < 128)
                                    {
                                        flag1 = true;
                                    }
                                }
                            }
                            for (n = 0; n < 4; n++)
                            {
                                byte num14 = 0;
                                byte num15 = 1;
                                for (o = 0; o < 4; o++)
                                {
                                    pixel = img.GetPixel(l * 4 + o, m * 4 + n);
                                    if (pixel.A >= 128)
                                    {
                                        List<Color> colors1 = new List<Color>();
                                        colors1.AddRange(this.palettes[this.paletteNumbers[l, m]]);
                                        if (flag1)
                                        {
                                            colors1.RemoveAt(3);
                                        }
                                        num = ImageIndexer.closest(pixel, colors1.ToArray());
                                    }
                                    else
                                    {
                                        num = 3;
                                    }
                                    num14 = (byte)(num14 | (byte)(num15 * num));
                                    num15 = (byte)(num15 * 4);
                                }
                                byteArrayOutputStream.writeByte(num14);
                            }
                            ushort num16 = (ushort)(numArray[this.paletteNumbers[l, m]] * 2);
                            if (!flag1)
                            {
                                num16 = (ushort)(num16 | 32768);
                            }
                            byteArrayOutputStream1.writeUShort(num16);
                        }
                    }
                    this.f5data = byteArrayOutputStream1.getArray();
                    this.texdata = byteArrayOutputStream.getArray();
                    break;
                }
            }
        }

        public int calcPaletteDiffs(int pal)
        {
            int num = -1;
            float single = 2.14748365E+09f;
            for (int i = 0; i < this.palettes.Count; i++)
            {
                if (this.paletteCounts[i] != 0)
                {
                    float[,] singleArray = this.paletteDiffs;
                    float[,] singleArray1 = this.paletteDiffs;
                    float single1 = this.palDif(this.palettes[pal], this.palettes[i]);
                    float single2 = single1;
                    singleArray1[i, pal] = single1;
                    singleArray[pal, i] = single2;
                }
                if (this.paletteDiffs[pal, i] < single)
                {
                    single = this.paletteDiffs[pal, i];
                    num = i;
                }
            }
            Console.Out.WriteLine(single);
            return -1;
        }

        public int contains(Color[][] c, Color[] a)
        {
            int num;
            int num1 = 0;
            while (true)
            {
                if (num1 < (int)c.Length)
                {
                    int num2 = 0;
                    for (int i = 0; i < (int)a.Length; i++)
                    {
                        if (c[num1][i] == a[i])
                        {
                            num2++;
                        }
                    }
                    if (num2 != (int)c[num1].Length)
                    {
                        num1++;
                    }
                    else
                    {
                        num = num1;
                        break;
                    }
                }
                else
                {
                    num = -1;
                    break;
                }
            }
            return num;
        }

        private bool ContainsTransparent(Bitmap image)
        {
            bool flag;
            int num = 0;
            while (true)
            {
                if (num < image.Height)
                {
                    int num1 = 0;
                    while (num1 < image.Width)
                    {
                        if (image.GetPixel(num1, num).A >= 128)
                        {
                            num1++;
                        }
                        else
                        {
                            flag = true;
                            return flag;
                        }
                    }
                    num++;
                }
                else
                {
                    flag = false;
                    break;
                }
            }
            return flag;
        }

        public int countUsedPalettes()
        {
            int num = 0;
            for (int i = 0; i < this.paletteCounts.Count; i++)
            {
                if (this.paletteCounts[i] != 0)
                {
                    num++;
                }
            }
            return num;
        }

        public int getClosestColor(Color c, Color[] pal)
        {
            int num = 0;
            float single = ImageIndexer.colorDifferenceWithoutAlpha(pal[0], c);
            for (int i = 0; i < (int)pal.Length; i++)
            {
                float single1 = ImageIndexer.colorDifferenceWithoutAlpha(pal[i], c);
                if (single1 < single)
                {
                    single = single1;
                    num = i;
                }
            }
            return num;
        }

        public int getClosestColorWithAlpha(Color c, Color[] pal)
        {
            int num = 0;
            float single = ImageIndexer.colorDifference(pal[0], c);
            for (int i = 0; i < (int)pal.Length; i++)
            {
                float single1 = ImageIndexer.colorDifference(pal[i], c);
                if (single1 < single)
                {
                    single = single1;
                    num = i;
                }
            }
            return num;
        }

        public float palDif(Color[] a, Color[] b)
        {
            float single = this.palDifUni(a, b) + this.palDifUni(b, a);
            return single;
        }

        public float palDifUni(Color[] a, Color[] b)
        {
            float single;
            bool flag = a[3] == Color.Transparent;
            if (flag == b[3] == Color.Transparent)
            {
                float single1 = 0f;
                int num = (flag ? 3 : 4);
                bool[] flagArray = new bool[num];
                for (int i = 0; i < num; i++)
                {
                    Color color = a[i];
                    float single2 = float.PositiveInfinity;
                    int num1 = -1;
                    for (int j = 0; j < num; j++)
                    {
                        if (!flagArray[j])
                        {
                            float single3 = ImageIndexer.colorDifference(color, b[j]);
                            if ((single3 < single2 ? true : num1 == -1))
                            {
                                num1 = j;
                                single2 = single3;
                            }
                        }
                    }
                    flagArray[num1] = true;
                    single1 += single2;
                }
                single = single1;
            }
            else
            {
                single = float.PositiveInfinity;
            }
            return single;
        }

        public Color[] palMerge(Color[] a, Color[] b)
        {
            bool flag = false;
            Bitmap bitmap = new Bitmap(8, 1);
            for (int i = 0; i < 4; i++)
            {
                bitmap.SetPixel(i, 0, a[i]);
                bitmap.SetPixel(i + 4, 0, b[i]);
                if ((b[i] == Color.Transparent ? true : a[i] == Color.Transparent))
                {
                    flag = true;
                }
            }
            List<Color> colors = new List<Color>();
            colors.AddRange(ImageIndexer.createPaletteForImage(bitmap, (flag ? 3 : 4), false));
            if (flag)
            {
                colors.Add(Color.Transparent);
            }
            return colors.ToArray();
        }

        @staticmethod
        def transparentToTheEnd(pal):
            transpFound = False

            for i in range(len(pal)):
                c = pal[i]
                if c[4] < 128:
                    pal[i] = pal[-1]
                    transpFound = True

            if transpFound:
                pal[-1] = (0, 0, 0, 0)
    }
}