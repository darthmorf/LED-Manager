using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
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
            PerformanceCounter gpuCounter;
            cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            ramCounter = new PerformanceCounter("Memory", "% Committed Bytes In Use");
            //gpuCounter = new PerformanceCounter("RemoteFX Root GPU Management", "VRAM: Reserved % per GPU", "GPU 0");

            int delay = 250;

            while (true)
            {
                DateTime start = DateTime.Now;

                Image img = CaptureWindow(User32.GetDesktopWindow());

                Bitmap bmp = new Bitmap(img);
                FastBitmap fbmp = new FastBitmap(bmp);
                fbmp.LockImage();

                var list = new Dictionary<int, int>();
                for (int x = 0; x < bmp.Width; x+= 50)
                {
                    for (int y = 0; y < bmp.Height; y++)
                    {
                        int rgb = fbmp.GetPixel(x, y).ToArgb();
                        var added = false;
                        for (int i = 0; i < 10; i++)
                        {
                            if (list.ContainsKey(rgb + i))
                            {
                                list[rgb + i]++;
                                added = true;
                                break;
                            }
                            if (list.ContainsKey(rgb - i))
                            {
                                list[rgb - i]++;
                                added = true;
                                break;
                            }
                        }
                        if (!added)
                            list.Add(rgb, 1);
                    }
                }

                int mostCommon = list.Values.Max();
                Color value = Color.FromArgb(list.FirstOrDefault(x => x.Value == mostCommon).Key);

                DateTime color = DateTime.Now;

                Console.WriteLine($"{value.ToString()} { (color - start).ToString()} | {cpuCounter.NextValue()}% {ramCounter.NextValue()}% gpuCounter.NextValue()%");

                Thread.Sleep(delay);
                //Console.ReadLine();
            }           
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
