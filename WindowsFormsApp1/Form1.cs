using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Threading;
using System.IO.Compression;

namespace WindowsFormsApp3
{
    public partial class Form1 : Form
    {
        public List<string> Path=new List<string>();
        Thread CopyThread;

        public Form1()
        {
            InitializeComponent();
            Path.Add("nani");
            Path.Add("nani");
            textBox1.Text = "E:/temp/Archives";
            textBox2.Text = "E:/temp/qq";
        }

        private void toolStripSplitButton1_ButtonClick(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button4_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog temp = new FolderBrowserDialog();
            if (temp.ShowDialog() == DialogResult.OK)
            {
                //Get the path of specified file
                textBox2.Text = temp.SelectedPath;
                Check(textBox2);
                //Read the contents of the file into a stream
            }

        }
        private void button3_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog temp = new FolderBrowserDialog();
            if (temp.ShowDialog() == DialogResult.OK)
            {
                //Get the path of specified file
                textBox1.Text = temp.SelectedPath;
                Check(textBox1);
                //Read the contents of the file into a stream
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            button1.Enabled = false;
            checkBox1.Enabled = false;
            CopyThread = new Thread(new ThreadStart(Copy));
            CopyThread.Priority = ThreadPriority.Highest;
            CopyThread.Start();
            button2.Enabled = true;
            //            Copy();
            /*
             * как првавило кнопа разблокирова мы ее блокируем
             начало работы
             еще раз проверяем пути
                        
            */

        }
        private void button2_Click(object sender, EventArgs e)
        {
            CopyThread.Abort();
            button2.Enabled = false;
            CheckPath(sender,e);
        }

        private void helo()
        {
            MessageBox.Show("HElo", "i work", MessageBoxButtons.OK,
       MessageBoxIcon.Information, MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
        }

        private bool Check(TextBox temp) {
            if (!System.IO.Directory.Exists(temp.Text))
            {
                toolStripStatusLabel1.Text = "no correct" + temp.Text;
                temp.BackColor = Color.FromArgb(255, 192, 192);
                temp.ForeColor = Color.FromArgb(200, 40, 40);
                toolStripStatusLabel1.ForeColor = Color.FromArgb(200, 40, 40);
                return false;
            }
            else
            {
                toolStripStatusLabel1.Text = "correct";
                temp.BackColor = Color.FromArgb(255, 255, 255);
                temp.ForeColor = Color.FromArgb(50, 180, 50);
                toolStripStatusLabel1.ForeColor = Color.FromArgb(40, 200, 40);
//                button1.Enabled = true;
                return true;
            }
        }
        private void CheckPath(object sender, EventArgs e)
        {
            Path[0] = textBox1.Text;
            Path[1] = textBox2.Text;
            Check(textBox1);
            Check(textBox2);
            if (Check(textBox1)&&Check(textBox2))
                button1.Enabled = true;
            else
                button1.Enabled = false;
            //сдезь мути м проверку
            /*вызывается при измении тескта в текст боксах
             * и должно выводится соответвествуюшая инфа о коректности
             * так же отвечает за блокировку кнопок начала работы
             * по умолчанию блокированы
             */
        }

        private void recursiveCreateAllNewDirectory(string dir)
        {
            var dirs = from i in Directory.EnumerateDirectories(dir)
                       where true
                       select i;
            foreach (string cur_dir in dirs)
            {
                Directory.CreateDirectory(Path[1] + cur_dir.Substring(Path[0].Length));
//                recursiveCreateAllNewDirectory(cur_dir); наверное это неправиль тк оно создает папки внутри а тедолжны создаватся и прикопировании файла послесоздания папки с годом
            }
        }

        private void Copy() {
            /*
            err = 0;
            k = 0;
            MMax = 0;
            Cf = 0;
            */

            //беру список директорий 
            var dirs = from i in Directory.EnumerateDirectories(Path[0])
                       where true
                       select i;
            //            label3.Text = dirs.LongCount().ToString()+"-";

            recursiveCreateAllNewDirectory(Path[0]);
            //захожу в каждую директорию
            foreach (string cur_dir in dirs)
            {
                IEnumerable<string> files = from i in Directory.EnumerateFiles(cur_dir, "*.pdf", SearchOption.AllDirectories)
                            where (/*File.GetCreationTime(i).Year*/File.GetLastWriteTime(i).Year <= DateTime.Now.Year)
                            select i;
//                BeginInvoke((MethodInvoker)(() => label3.Text = "-" + files.LongCount().ToString() ));//количество файлов в папке
//                BeginInvoke((MethodInvoker)(()=>toolStripProgressBar1.Maximum = Convert.ToInt32(files.LongCount())));
                Invoke((MethodInvoker)(() => toolStripProgressBar1.Maximum = Convert.ToInt32(files.LongCount())));
//                BeginInvoke((MethodInvoker)(() => toolStripProgressBar1.Value = 0));
                Invoke((MethodInvoker)(() => toolStripProgressBar1.Value = 0));
                foreach (string file in files)
                {
                    //не понятно зачем label4.инвоке елси можно просто инвоке
                    label4.Invoke((MethodInvoker)(() => label4.Text = file));
//                    BeginInvoke((MethodInvoker)(() => toolStripProgressBar1.PerformStep()));
                    Invoke((MethodInvoker)(() => toolStripProgressBar1.PerformStep()));
                    if (!System.IO.Directory.Exists(Path[1] + cur_dir.Substring(Path[0].Length) + "/" + /*File.GetCreationTime(file).Year*/File.GetLastWriteTime(file).Year))
                    {
                        Directory.CreateDirectory(Path[1] + cur_dir.Substring(Path[0].Length)+ "/" + /*File.GetCreationTime(file).Year*/File.GetLastWriteTime(file).Year);
                    }
                    string fileto = Path[1] + cur_dir.Substring(Path[0].Length) + "/" + /*File.GetCreationTime(file).Year*/File.GetLastWriteTime(file).Year + "/"+ file.Substring(cur_dir.Length);
                    //я это не хотел
                    FileInfo f = new FileInfo(file);
                    if (!System.IO.Directory.Exists(fileto.Substring(0,fileto.Length-f.Name.Length)))
                    {
                        Directory.CreateDirectory(fileto.Substring(0, fileto.Length - f.Name.Length));
                    }

                    //                    string fileto = Path[1] + File.GetCreationTime(file).Year + file.Substring(Path[0].Length);//тута сделать что надото. шта?соглашусь, шта? кажизьсь тута прсто копирование, бес сортивки погодам ппц.
                    try
                    { 
                        File.Copy(file, fileto, checkBox1.Checked);
                    }
                    catch (System.IO.IOException)
                    {
                        continue;
                    }
                }
            }
            label4.Invoke((MethodInvoker)(() => label4.Text = "END"));
            Invoke((MethodInvoker)(()=> checkBox1.Enabled = true));
/*            MessageBox.Show("Закончено копирование","Сообшение о завершении", MessageBoxButtons.OK,
        MessageBoxIcon.Information,MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
*/
            //идут работы || 
            //           \  /
            //            \/
            dirs = from i in Directory.EnumerateDirectories(Path[1])
                       where true
                       select i;
            foreach (string cur_dir in dirs)
            {
                var ZipDirs = from i in Directory.EnumerateDirectories(cur_dir)
                       where true
                       select i;
                foreach (string zip_dir in ZipDirs)
                {

                    if (!System.IO.File.Exists(zip_dir + ".zip"))
                        ZipFile.CreateFromDirectory(zip_dir, zip_dir + ".zip", CompressionLevel.Optimal, false);
                    else
                    {
                        ZipArchive Zip = ZipFile.Open(zip_dir + ".zip", ZipArchiveMode.Update);

                        IEnumerable<string> files = from i in Directory.EnumerateFiles(zip_dir, "*.pdf", SearchOption.AllDirectories)
                                                    where (/*File.GetCreationTime(i).Year*/File.GetLastWriteTime(i).Year <= DateTime.Now.Year)
                                                    select i;
                        foreach (string file in files)
                            Zip.CreateEntryFromFile(file,file.Substring(zip_dir.Length+1));
                        Zip.Dispose();
                    }
                }
            }


            /* сделано /\/\/\/\/\
            /*
            try
            {
                out_label['text'] = ("обнаружено" + str(MMax))////
                }
            catch BaseException
            { c = 0; }
            for direc in os.listdir(dir_src):{
                direc_src = os.path.join(dir_src, direc)
            //        print(direc_src)
                    for root, dirs, files in os.walk(direc_src):
                //        print ("[-]"+dir_src+dir_dst+str(stop))
                            for name in files:{
// print ("[-]"+dir_src+dir_dst)
                        f_src = os.path.join(root, name)
                                temptime = datetime.datetime.fromtimestamp(os.path.getmtime(f_src))
                        try:
                    //            print ("[-]"+dir_src+dir_dst)
                                    k = k + 1
                                        out_label['text'] = ("обработано " + str(k - 1) + "/" + str(MMax) + "\n" + f_src)////
                                except BaseException:
                                    c = 0
                                    if temptime.year != date.year:{
// путь к файлу назначения
                            f_dst = dir_dst + "/" + direc + "/" + str(temptime.year) + "/" + (f_src[len(direc_src):len(root)]) + "/" + name
                  //                    f_dst=dir_dst+f_src[len(dir_src):len(root)]+"/"++"/"+name
                                    //путь к папке назначения
                                    p_dst = dir_dst + "/" + direc + "/" + str(temptime.year) + "/" + (f_src[len(direc_src):len(root)])
                  //                    p_dst=dir_dst+f_src[len(dir_src):len(root)]+"/"+str(temptime.year)+"/"
                                    if not os.path.exists(f_dst):{
// print ("[-] ", f_src)
                                temp = datetime.datetime.now()
                                        log.write("" + str(temp.day) + "/" + str(temp.month) + "/" + str(temp.year) + " " + str(temp.hour) + ":" + str(temp.minute) + ":" + str(temp.second) + " copy " + f_src + " to " + f_dst + "\n")
                                        //создание директории если отсутсвует
                                        if not os.path.exists(p_dst):
                                            os.makedirs(p_dst)
                                        shutil.copy2(f_src, f_dst)
                                        Cf = Cf + 1
                    //                    os.system("xcopy "+f_src+" "+p_dst+" /z /y /v /i")
                    //                    log.write(str(subprocess.check_output("xcopy \""+f_src+"\" \""+p_dst+"\" /z /y /v")))
                                        }
                                    else:
                                        if (zap == 0 and not filecmp.cmp(f_src, f_dst) and not compare_h(f_src) == compare_h(f_dst)){
                                i = 0
                                                name = name[:name.find('(')] + name[name.find(')'):]
                                                while (os.path.exists(f_dst)){
                    i = i + 1;
                                                f_dst = p_dst + "/" + name[:name.find('.')] + "(" + str(i) + ")" + name[name.find('.'):]}
// print(f_dst)
                                shutil.copy2(f_src, f_dst)
                                                Cf = Cf + 1}
                            while (! filecmp.cmp(f_src, f_dst) and not compare_h(f_src) == compare_h(f_dst) && err<5){
// print ("измененый файл , перезапись ", f_src)
                                temp = datetime.datetime.now()
                                              log.write("" + str(temp.day) + "/" + str(temp.month) + "/" + str(temp.year) + " " + str(temp.hour) + ":" + str(temp.minute) + ":" + str(temp.second) + " compare erro, rewrite " + f_src + " to " + f_dst + "\n")
                          //                    log.write(str(subprocess.check_output("xcopy \""+f_src+"\" \""+p_dst+"\" /z /y /v")))
                    //                    os.system("xcopy "+f_src+" "+p_dst+" /z /y /v /i")
                    //                    subprocess.run(['xcopy', os.path.abspath(f_src), os.path.abspath(p_dst),'/s', '/e', '/z', '/y', '/v', '/i'],"log.log")

                                        shutil.copy2(f_src, f_dst)
                                              err = err + 1
                          //                    shutil.copy2(f_src,f_dst)}
                                    if (err == 5){
                                        temp = datetime.datetime.now()
                                          log.write("" + str(temp.day) + "/" + str(temp.month) + "/" + str(temp.year) + " " + str(temp.hour) + ":" + str(temp.minute) + ":" + str(temp.second) + " rewrite File: " + f_src + " failed\n")
                                      }else{
                                    temp = datetime.datetime.now()
                                          log.write("" + str(temp.day) + "/" + str(temp.month) + "/" + str(temp.year) + " " + str(temp.hour) + ":" + str(temp.minute) + ":" + str(temp.second) + " " + str(err) + " rewrite " + f_src + "\n")
                                          os.remove(f_src)
                                          log.write(" remove " + f_src + "\n")}
                                err = 0
                          }
                        }

                        }*/

            MessageBox.Show("Закончено архивирование", "Сообшение о завершении", MessageBoxButtons.OK,
        MessageBoxIcon.Information, MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
            Invoke((MethodInvoker)(() => button2.Enabled = false));
        }

        private void checkBox2_CheckedChanged(object sender, EventArgs e)
        {

        }

    }
}
