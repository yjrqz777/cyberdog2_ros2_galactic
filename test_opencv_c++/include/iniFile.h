#ifndef INIFILE_H_ 
#define INIFILE_H_

#include <string>
#include <string.h>
#include <map>
#include <vector>
#include <fstream>
#include <algorithm>

#define MAX_FILEPATH  256
#define MAX_ROWLEN  256
#define MIDDLESTRING "/" 

typedef std::map<std::string, std::string> INIMap; 
typedef INIMap::iterator MapIter; 

struct IniAnalyze : public std::unary_function<void, const std::string &>
{ 
private:
	std::string m_strSection; // Section

	INIMap *m_pMap; 
public:
	IniAnalyze(INIMap &IniMap)
		: m_pMap(&IniMap)
		, m_strSection("")
	{
	}

	// ÖØÔØ(), ·Âº¯Êý
	void operator()(const std::string &strIni) 
	{ 
		std::string::size_type first =strIni.find('[');
		std::string::size_type last = strIni.rfind(']');
		if ((std::string::npos != first) && (std::string::npos != last) && (first != last+1))
		{
			m_strSection = strIni.substr(first + 1,last - first - 1);
			return ;
		}

		if (m_strSection.empty())
		{
			return ;
		}
		if (std::string::npos == (first = strIni.find('=')))
		{
			return ;
		}
		std::string strKey = strIni.substr(0, first);
		std::string strValue =strIni.substr(first + 1, std::string::npos);
		first = strKey.find_first_not_of(" \t");
		last = strKey.find_last_not_of(" \t");
		if ((std::string::npos == first) || (std::string::npos == last))
		{
			return ;
		}
		strKey = strKey.substr(first, last-first+1);

		first = strValue.find_first_not_of(" \t");
		if ((std::string::npos != (last = strValue.find("\t#", first ))) || \
			(std::string::npos != (last = strValue.find(" #", first ))) || \
			(std::string::npos != (last = strValue.find("\t//", first ))) || \
			(std::string::npos != (last = strValue.find(" //", first ))))
		{
			strValue = strValue.substr(0, last - first);
		}
		last = strValue.find_last_not_of(" \t");
		if ((first == std::string::npos) || (std::string::npos == last))
		{
			return ;
		}
		strValue = strValue.substr(first, last - first + 1);
		std::string mapkey = m_strSection + MIDDLESTRING;
		mapkey += strKey;
		(*m_pMap)[mapkey] = strValue;
		return ;
	} 
}; 

class IniFile 
{ 
public: 
	IniFile(const char *szIniFile) 
	{ 
		memset(m_szIniFile, 0, MAX_FILEPATH);
		size_t nLen = strlen(szIniFile);
		if (nLen <= MAX_FILEPATH - 1)
		{
			memcpy(m_szIniFile, szIniFile, nLen); 
			do_open(m_szIniFile); 
		}
	}; 

	~IniFile() 
	{ 
	}; 

	void Updae(void) 
	{ 
		writeini(m_szIniFile); 
	} 

	char *readstring(const char *pSect, const char *pKey, char *szDefault, unsigned int &nSize)
	{ 
		std::string strKey = pSect; 
		strKey += MIDDLESTRING; 
		strKey += pKey; 

		MapIter it = m_iniMap.begin();
		it = m_iniMap.find(strKey); 
		if (it == m_iniMap.end()) 
		{ 
			return szDefault;
		} 

		nSize = it->second.size();
		return (char *)it->second.c_str();

	}; 

	void writestring(const char *pSect, const char *pKey, char *pValue) 
	{
		std::string strKey = pSect; 
		strKey += MIDDLESTRING; 
		strKey += pKey; 

		MapIter it = m_iniMap.find(strKey); 
		if (it != m_iniMap.end()) 
		{ 
			it->second = pValue; 
			return; 
		} 
		m_iniMap[strKey] = pValue; 
	}; 

	int readinteger(const char *pSect, const char *pKey, int iValue = 0) 
	{ 
		unsigned int nSize = 0;
		const char *pValue = readstring(pSect, pKey, NULL, nSize); 
		if (NULL == pValue) 
		{ 
			return iValue; 
		} 
		return atoi(pValue); 
	} 

	void writeinteger(const char *pSect, const char *pKey, int iValue) 
	{ 
		char szValue[32] = {'\0'};
#if (defined(_MSC_VER) && (_MSC_VER > 1400))
		sprintf_s(szValue, sizeof(szValue) - 1, "%d", iValue); 
#else
		sprintf(szValue, "%d", iValue); 
#endif
		writestring(pSect, pKey, szValue); 
	} 

	double readdouble(const char *pSect, const char *pKey, double dValue = 0) 
	{ 
		unsigned int nSize = 0;
		const char *pValue = readstring(pSect, pKey, NULL, nSize); 
		if (NULL == pValue) 
		{ 
			return dValue; 
		} 
		return atof(pValue); 
	} 

	void writedouble(const char *pSect, const char *pKey, double dValue) 
	{ 
		char szValue[32] = {'\0'};
#if (defined(_MSC_VER) && (_MSC_VER > 1400))
		sprintf_s(szValue, sizeof(szValue) - 1, "%f", dValue); 
#else
		sprintf(szValue, "%f", dValue); 
#endif
		writestring(pSect, pKey, szValue); 
	} 

	bool readbool(const char *pSect, const char *pKey, bool bValue = false) 
	{ 
		unsigned int nSize = 0;
		const char *pValue = readstring(pSect, pKey, NULL, nSize); 
		if (NULL == pValue) 
		{ 
			return bValue; 
		} 
		return strcmp(pValue, "1") == 0 ? true : false; 
	} 

	void writebool(const char *pSect, const char *pKey, bool bValue) 
	{ 
		char szValue[2] = {0}; 
		szValue[0] = '0'; 
		if (bValue) szValue[0] = '1'; 
		writestring(pSect, pKey, szValue); 
	} 

	void deletekey(const char *pSect, const char *pKey) 
	{ 
		std::string mapkey = pSect; 
		mapkey += MIDDLESTRING; 
		mapkey += pKey; 

		MapIter it = m_iniMap.find(mapkey); 
		if (it != m_iniMap.end()) 
		{ 
			m_iniMap.erase(it); 
		} 
	} 

	void deletesection(const char *pSect) 
	{ 
		MapIter it; 
		std::string sSess, m_strSect; 
		std::string::size_type uPos = 0; 
		for (it = m_iniMap.begin(); it != m_iniMap.end(); ++it) 
		{ 
			m_strSect = it->first; 
			uPos = m_strSect.find(MIDDLESTRING); 
			sSess = m_strSect.substr(0, uPos); 
			if (sSess == pSect) 
			{ 
				m_iniMap.erase(it); 
			} 
		} 
	} 

private: 

	char m_szIniFile[MAX_FILEPATH];

	INIMap m_iniMap; 

	bool do_open(const char *pIniFile) 
	{ 
		std::ifstream fin(pIniFile); 
		if (!fin.is_open()) 
		{ 
			return false; 
		} 

		std::vector<std::string> strVect; 
		std::string strLine = ""; 
		while(!fin.eof()) 
		{ 
			getline(fin, strLine, '\n'); 
			strVect.push_back(strLine); 
		} 
		fin.close(); 

		if (strVect.empty()) 
		{ 
			return false; 
		} 

		std::for_each(strVect.begin(), strVect.end(), IniAnalyze(m_iniMap)); 

		return !m_iniMap.empty(); 
	}


	bool writeini(const char *pIniFile) 
	{ 
		if (m_iniMap.empty()) 
		{ 
			return false; 
		} 

		std::ofstream fout(pIniFile); 
		if (!fout.is_open()) 
		{ 
			return false; 
		} 

		MapIter it; 
		unsigned int iMID_LEN = strlen(MIDDLESTRING); 
		std::string sSessSave = "", sSess, sKey, m_strSect; 
		std::string::size_type uPos = 0; 
		for (it = m_iniMap.begin(); it != m_iniMap.end(); ++it) 
		{ 
			m_strSect = it->first; 
			uPos = m_strSect.find(MIDDLESTRING); 
			sSess = m_strSect.substr(0, uPos); 
			if (sSessSave != sSess) 
			{ 
				sSessSave = sSess; 
				fout << "[" << sSess << "]" << std::endl; 
			} 

			sKey = m_strSect.substr(uPos + iMID_LEN, strlen(m_strSect.c_str()) - uPos - iMID_LEN); 
			fout << sKey << "=" << it->second << "" << std::endl; 
		} 

		fout.close(); 
		return true; 
	} 
}; 

#endif // #ifndef INIFILE_H_ 

