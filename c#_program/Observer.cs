using System.Net;

namespace newsPortal
{
    class Observer
    {
        private object Lock = new object();
        private int SleepTime;
        private FileLogger ProcessedArticleWriter = new FileLogger("processed_articles.txt");
        private FileLogger WorkerLogger = new FileLogger("logs.txt");
        private RSSReader RssReader;

        private int OldArticles = 0;
        private int RssLentsProcessed = 0;
        private int NewArticles = 0;
        public Observer(int sleepTime = 1)
        {
            SleepTime = sleepTime * 1000 * 60;
            RssReader = new RSSReader();
        }
        public void Observe()
        {
            while (true)
            {
                NewArticles = 0;
                OldArticles = 0;
                RssLentsProcessed = 0;
                UpdateNews();
                WorkerLogger.Logging($"За текущую итерацию получено {NewArticles} новых статей и {OldArticles} старых статей. Всего обработано - {NewArticles + OldArticles} статей");
                WorkerLogger.Logging($"За текущую итерацию обработано {RssLentsProcessed} rss лент");
                Thread.Sleep(SleepTime);
            }
        }
        public void UpdateNews()
        {
            List<Task<int>> tasks = new List<Task<int>>();
            using (StreamReader reader = new StreamReader("rss_list.txt"))
            {
                while (reader.Peek() >= 0)
                {
                    string str = reader.ReadLine();
                    if (str == null || str.Length == 0)
                    {
                        break;
                    }
                    Task<int> task = new Task<int>(() => MethodForThread(str));
                    task.Start();
                    tasks.Add(task);
                }
            }
            Task.WaitAll(tasks.ToArray());
        }
        int MethodForThread(string url)
        {
            WorkerLogger.Logging("RSS лента " + url + " взята в обработку!");
            List<string> links = RssReader.Read(url);
            foreach (string link in links)
            {
                // save info about article
                WebRequest request = WebRequest.Create(link);
                WebResponse response = request.GetResponse();

                // update article info
                using (StreamReader reader = new StreamReader("processed_articles.txt"))
                {
                    bool isProcessed = false;
                    Monitor.Enter(Lock);
                    while (reader.Peek() >= 0)
                    {
                        if (reader.ReadLine() == link)
                        {
                            isProcessed = true;
                            break;
                        }
                    }
                    try
                    {
                        if (!isProcessed)
                        {
                            NewArticles++;
                            WorkerLogger.Logging("Появилась новая статья : " + link);
                            ProcessedArticleWriter.Logging(link);
                            ProcessUnprocessedArticle(link);
                            WorkerLogger.Logging("Статья " + link + " скачана!");
                        }
                        else
                        {
                            OldArticles++;
                        }
                    }
                    finally
                    {
                        Monitor.Exit(Lock);
                    }

                }
            }
            RssLentsProcessed++;
            WorkerLogger.Logging("RSS лента " + url + " обработана!");
            return 0;
        }
        async void ProcessUnprocessedArticle(string link)
        {
            // process unprocessed_article
            Uri uri = new Uri(link);
            string path = $"./articles/{uri.Host}";

            // create directory
            if (!Directory.Exists(path))
            {
                try
                {
                    Directory.CreateDirectory(path);
                }
                catch (Exception exc)
                {
                    WorkerLogger.Logging($"Перехвачено исключение: {exc.Message}");
                }
            }

            // download
            try
            {
                using (var webClient = new WebClient())
                {
                    string filename = link.Replace('/', '_') + ".html";
                    await webClient.DownloadFileTaskAsync(link, path + "/" + filename);
                }
            }
            catch (Exception exc)
            {
                WorkerLogger.Logging($"Перехвачено исключение: {exc.Message}");
            }

        }
    }
}