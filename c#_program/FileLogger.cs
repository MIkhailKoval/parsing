namespace newsPortal
{
    public class FileLogger : ILogger
    {
        public string filename;
        public FileLogger(string filename)
        {
            this.filename = filename;
        }
        public void Logging(string message)
        {
            using (var writer = new StreamWriter(this.filename, true))
            {
                writer.WriteLine(message);
            }
        }
    }
}