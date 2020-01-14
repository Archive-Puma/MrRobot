use crate::Colorize;

#[derive(Debug)]
pub struct Report {
    rtype: ReportType,
    report: String
}

#[derive(Debug)]
pub enum ReportType {
    Stdout
}

impl Report {
    pub fn new(kind: &str) -> Self {
        let report: String = String::new();
        match kind {
            "stdout" => Report{ report: report, rtype: ReportType::Stdout },
            _ => Report{ report: report, rtype: ReportType::Stdout }
        }
    }
    pub fn to_str(&self) -> &str {
        &self.report
    }
    pub fn append(&mut self, text: String) {
        let report: String = String::from(self.to_str());
        self.report = [report,text].join("\n");
    }
    pub fn format(&self, number: usize) -> String {
        let limit: usize = if number < 40 { 40 } else if number > 115 { 115 } else { number };
        let mut result: Vec<String> = Vec::new();
        for line in self.to_str().lines() {
            let mut text: String = line.to_string();
            while text.len() > limit {
                let segment: String = text.chars().take(limit).collect();
                let ending:  String = text.chars().skip(limit).collect();
                result.push(segment.to_string());
                text = ending;
            }
            if text.len() > 0 { result.push(text.to_string()); }
        }
        result.iter().fold(String::new(), |result, segment| [result,segment.to_string()].join("\n"))
        .trim().to_string()
    }
    pub fn display(&self, limit: usize) {
        let report: Vec<String> = self.format(limit).lines()
            .map(|line| format!(" {} {}", "|", line)).collect();
        println!("{} {}\n{}", "[+]".bold(), "Execution result:", report.join("\n"));
    }
}
