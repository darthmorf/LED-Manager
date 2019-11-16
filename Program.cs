using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace LEDManager
{
    class Program
    {
        public static void Main(string[] args)
        {
            PerformanceCounter cpuCounter;
            PerformanceCounter ramCounter;
            cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            ramCounter = new PerformanceCounter("Memory", "% Committed Bytes In Use");
            GPUMonitor gpuCounter = new GPUMonitor();

            Color screenColor;
            float cpuValue;
            float ramValue;
            float gpuValue;

            List<Color> colors = new List<Color>();

            foreach (System.Reflection.PropertyInfo prop in typeof(Color).GetProperties())
            {
                if (prop.PropertyType.FullName == "System.Drawing.Color")
                    colors.Add(Color.FromName(prop.Name));
            }

            List<Color> bannedColors = new List<Color>() { Color.Transparent, Color.Black, Color.Gray, Color.LightSlateGray, Color.DimGray, Color.SlateGray, Color.DarkGray };

            colors = colors.Except(bannedColors).ToList();

            //LEDGrid ledGrid = new LEDGrid();
            UdpClient client = new UdpClient("127.0.0.1",2610);

            int delay = 250;

            while (true)
            {
                screenColor = getScreenColor(colors);
                cpuValue = cpuCounter.NextValue();
                ramValue = ramCounter.NextValue();
                gpuValue = gpuCounter.GetGpuInfo();

                Console.WriteLine($"{screenColor.ToString()} {cpuValue}% {ramValue}% {gpuValue}%");
                byte[] bytes = StatusPacket.NewStatusPacket(screenColor, cpuValue, ramValue, gpuValue);
                client.Send(bytes, bytes.Length);

                Thread.Sleep(delay);
            }
        }

        public static Color getScreenColor(List<Color> allColors)
        {
            Image img = CaptureWindow(User32.GetDesktopWindow());

            Bitmap bmp = new Bitmap(img);
            FastBitmap fbmp = new FastBitmap(bmp);
            fbmp.LockImage();

            Dictionary<Color, int> colors = new Dictionary<Color, int>();
            for (int x = 0; x < bmp.Width; x += 50)
            {
                for (int y = 0; y < bmp.Height; y++)
                {
                    Color color = fbmp.GetPixel(x, y);
                    color = closestColor(allColors, color);
                    if (colors.ContainsKey(color))
                    {
                        colors[color]++;
                    }
                    else
                    {
                        colors.Add(color, 1);
                    }
                }
            }

            int mostCommon = colors.Values.Max();
            return colors.FirstOrDefault(x => x.Value == mostCommon).Key;
        }

        static Color closestColor(List<Color> colors, Color target)
        {
            var hue1 = target.GetHue();
            var diffs = colors.Select(n => getHueDistance(n.GetHue(), hue1));
            var diffMin = diffs.Min(n => n);
            return colors[diffs.ToList().FindIndex(n => n == diffMin)];
        }

        static float getHueDistance(float hue1, float hue2)
        {
            float d = Math.Abs(hue1 - hue2); return d > 180 ? 360 - d : d;
        }

        public static Image CaptureWindow(IntPtr handle)
        {
            // get te hDC of the target window
            IntPtr hdcSrc = User32.GetWindowDC(handle);
            // get the size
            User32.RECT windowRect = new User32.RECT();
            User32.GetWindowRect(handle, ref windowRect);
            int width = windowRect.right - windowRect.left;
            int height = windowRect.bottom - windowRect.top;
            // create a device context we can copy to
            IntPtr hdcDest = GDI32.CreateCompatibleDC(hdcSrc);
            // create a bitmap we can copy it to,
            // using GetDeviceCaps to get the width/height
            IntPtr hBitmap = GDI32.CreateCompatibleBitmap(hdcSrc, width, height);
            // select the bitmap object
            IntPtr hOld = GDI32.SelectObject(hdcDest, hBitmap);
            // bitblt over
            GDI32.BitBlt(hdcDest, 0, 0, width, height, hdcSrc, 0, 0, GDI32.SRCCOPY);
            // restore selection
            GDI32.SelectObject(hdcDest, hOld);
            // clean up 
            GDI32.DeleteDC(hdcDest);
            User32.ReleaseDC(handle, hdcSrc);
            // get a .NET image object for it
            Image img = Image.FromHbitmap(hBitmap);
            // free up the Bitmap object
            GDI32.DeleteObject(hBitmap);
            return img;
        }
    }

    public static class StatusPacket
    {
        struct Data
        {
            public int colorA;
            public int colorR;
            public int colorG;
            public int colorB;
            public float cpuUsage;
            public float ramUsage;
            public float gpuUsage;
        }

        public static byte[] NewStatusPacket(Color color, float cpuUsage, float ramUsage, float gpuUsage)
        {
            Data data = new Data();
            data.colorA = color.A;
            data.colorR = color.R;
            data.colorG = color.G;
            data.colorB = color.B;
            data.cpuUsage = cpuUsage;
            data.ramUsage = ramUsage;
            data.gpuUsage = gpuUsage;


            int size = Marshal.SizeOf(data);
            byte[] arr = new byte[size];

            IntPtr ptr = Marshal.AllocHGlobal(size);
            Marshal.StructureToPtr(data, ptr, true);
            Marshal.Copy(ptr, arr, 0, size);
            Marshal.FreeHGlobal(ptr);
            return arr;
        }
    }

    public class LEDGrid : List<List<Color>>
    {
        private int Width;
        private int Height;
        public LEDGrid (int width = 32, int height = 32)
        {
            Width = width;
            Height = height;

            Color defaultColor = Color.Cyan;;

            for (int x = 0; x < width; x++)
            {
                List<Color> column = new List<Color>();
                for (int y = 0; y < height; y++)
                {
                    column.Add(defaultColor);
                }
                Add(column);
            }
        }
        public Color get(int x, int y)
        {
            return this[x][y];
        }

        public void set(int x, int y, Color color)
        {
            this[x][y] = color;
        }

        public byte[] ToBytes()
        {
            byte[] bytes = new byte[Width*Height*4];

            int i = 0;
            foreach (List<Color> column in this)
            {
                foreach (Color color in column )
                {
                    bytes[i++] = color.A;
                    bytes[i++] = color.R;
                    bytes[i++] = color.B;
                    bytes[i++] = color.G;
                }
            }

            return bytes;
        }
    }

    unsafe public class FastBitmap
    {
        private struct PixelData
        {
            public byte blue;
            public byte green;
            public byte red;
            public byte alpha;

            public override string ToString()
            {
                return "(" + alpha.ToString() + ", " + red.ToString() + ", " + green.ToString() + ", " + blue.ToString() + ")";
            }
        }

        private Bitmap workingBitmap = null;
        private int width = 0;
        private BitmapData bitmapData = null;
        private Byte* pBase = null;

        public FastBitmap(Bitmap inputBitmap)
        {
            workingBitmap = inputBitmap;
        }

        public void LockImage()
        {
            Rectangle bounds = new Rectangle(Point.Empty, workingBitmap.Size);

            width = (int)(bounds.Width * sizeof(PixelData));
            if (width % 4 != 0) width = 4 * (width / 4 + 1);

            //Lock Image
            bitmapData = workingBitmap.LockBits(bounds, ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
            pBase = (Byte*)bitmapData.Scan0.ToPointer();
        }

        private PixelData* pixelData = null;

        public Color GetPixel(int x, int y)
        {
            pixelData = (PixelData*)(pBase + y * width + x * sizeof(PixelData));
            return Color.FromArgb(pixelData->alpha, pixelData->red, pixelData->green, pixelData->blue);
        }

        public Color GetPixelNext()
        {
            pixelData++;
            return Color.FromArgb(pixelData->alpha, pixelData->red, pixelData->green, pixelData->blue);
        }

        public void SetPixel(int x, int y, Color color)
        {
            PixelData* data = (PixelData*)(pBase + y * width + x * sizeof(PixelData));
            data->alpha = color.A;
            data->red = color.R;
            data->green = color.G;
            data->blue = color.B;
        }

        public void UnlockImage()
        {
            workingBitmap.UnlockBits(bitmapData);
            bitmapData = null;
            pBase = null;
        }
    }

    public class GDI32
    {

        public const int SRCCOPY = 0x00CC0020; // BitBlt dwRop parameter
        [DllImport("gdi32.dll")]
        public static extern bool BitBlt(IntPtr hObject, int nXDest, int nYDest,
            int nWidth, int nHeight, IntPtr hObjectSource,
            int nXSrc, int nYSrc, int dwRop);
        [DllImport("gdi32.dll")]
        public static extern IntPtr CreateCompatibleBitmap(IntPtr hDC, int nWidth,
            int nHeight);
        [DllImport("gdi32.dll")]
        public static extern IntPtr CreateCompatibleDC(IntPtr hDC);
        [DllImport("gdi32.dll")]
        public static extern bool DeleteDC(IntPtr hDC);
        [DllImport("gdi32.dll")]
        public static extern bool DeleteObject(IntPtr hObject);
        [DllImport("gdi32.dll")]
        public static extern IntPtr SelectObject(IntPtr hDC, IntPtr hObject);
    }

    /// <summary>
    /// Helper class containing User32 API functions
    /// </summary>
    public class User32
    {
        [StructLayout(LayoutKind.Sequential)]
        public struct RECT
        {
            public int left;
            public int top;
            public int right;
            public int bottom;
        }
        [DllImport("user32.dll")]
        public static extern IntPtr GetDesktopWindow();
        [DllImport("user32.dll")]
        public static extern IntPtr GetWindowDC(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern IntPtr ReleaseDC(IntPtr hWnd, IntPtr hDC);
        [DllImport("user32.dll")]
        public static extern IntPtr GetWindowRect(IntPtr hWnd, ref RECT rect);
    }
}
